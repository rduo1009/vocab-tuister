package navigator

import (
	"fmt"
)

type (
	AddNavigableMsg     struct{ Components []Navigable }
	RemoveNavigableMsg  struct{ IDs []string }
	ReplaceNavigableMsg struct {
		ID         string
		Components []Navigable
	}
	FocusNavigableMsg struct{ ID string }
)

// Navigable represents any component that can receive navigation focus.
type Navigable interface {
	SetFocused(bool)
	Focused() bool
	ID() string
}

// Navigator manages focus between multiple navigable components.
type Navigator struct {
	Items        []Navigable
	CurrentIndex int
}

func New(items []Navigable, index int) *Navigator {
	return &Navigator{
		Items:        items,
		CurrentIndex: index,
	}
}

func (n *Navigator) Next() {
	if len(n.Items) == 0 {
		return
	}

	n.Items[n.CurrentIndex].SetFocused(false)
	n.CurrentIndex = (n.CurrentIndex + 1) % len(n.Items)
	n.Items[n.CurrentIndex].SetFocused(true)
}

func (n *Navigator) Previous() {
	if len(n.Items) == 0 {
		return
	}

	n.Items[n.CurrentIndex].SetFocused(false)
	n.CurrentIndex = (n.CurrentIndex - 1 + len(n.Items)) % len(n.Items)
	n.Items[n.CurrentIndex].SetFocused(true)
}

func (n *Navigator) Current() Navigable {
	if len(n.Items) == 0 {
		return nil
	}

	return n.Items[n.CurrentIndex]
}

func (n *Navigator) Add(components ...Navigable) {
	oldLen := len(n.Items)
	n.Items = append(n.Items, components...)

	// If the list was empty before, set focus to the first item
	if oldLen == 0 && len(n.Items) > 0 {
		n.CurrentIndex = 0
		n.Items[0].SetFocused(true)
	}
}

func (n *Navigator) Remove(ids ...string) {
	for _, id := range ids {
		for i, item := range n.Items {
			if item.ID() == id {
				// Unfocus if removing current
				if i == n.CurrentIndex {
					item.SetFocused(false)

					if len(n.Items) > 1 {
						n.CurrentIndex = (i - 1 + len(n.Items)) % len(n.Items)
						n.Items[n.CurrentIndex].SetFocused(true)
					} else {
						n.CurrentIndex = 0
					}
				} else if i < n.CurrentIndex {
					n.CurrentIndex--
				}

				// Remove item
				n.Items = append(n.Items[:i], n.Items[i+1:]...)

				// Break inner loop to process next ID
				break
			}
		}
	}
}

func (n *Navigator) Replace(id string, components ...Navigable) {
	for i, item := range n.Items {
		if item.ID() == id {
			// Unfocus if replacing current
			wasFocused := (i == n.CurrentIndex)
			if wasFocused {
				item.SetFocused(false)
			}

			// Replace item with new components
			newItems := make([]Navigable, 0, len(n.Items)-1+len(components))
			newItems = append(newItems, n.Items[:i]...)
			newItems = append(newItems, components...)
			newItems = append(newItems, n.Items[i+1:]...)
			n.Items = newItems

			if len(n.Items) == 0 {
				n.CurrentIndex = 0

				return
			}

			if wasFocused {
				if len(components) > 0 {
					n.CurrentIndex = i
				} else {
					n.CurrentIndex = (i - 1 + len(n.Items)) % len(n.Items)
				}

				n.Items[n.CurrentIndex].SetFocused(true)
			} else if i < n.CurrentIndex {
				n.CurrentIndex += len(components) - 1
			}

			return
		}
	}
}

func (n *Navigator) Reset() {
	n.Items = n.Items[:1]
	n.CurrentIndex = 0
}

func (n *Navigator) FocusNavigable(id string) error {
	for i, item := range n.Items {
		if item.ID() == id {
			if i == n.CurrentIndex {
				return nil
			}

			n.Items[n.CurrentIndex].SetFocused(false)
			n.CurrentIndex = i
			n.Items[n.CurrentIndex].SetFocused(true)
			return nil
		}
	}

	return fmt.Errorf("navigable with id %s not found", id)
}
