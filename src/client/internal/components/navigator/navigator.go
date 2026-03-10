package navigator

import (
	"fmt"
)

type (
	AddNavigableMsg     struct{ Components []Navigable }
	RemoveNavigableMsg  struct{ Components []Navigable }
	ReplaceNavigableMsg struct {
		Target      Navigable
		Replacement []Navigable
	}
	FocusNavigableMsg struct{ Target Navigable }
)

// Navigable represents any component that can receive navigation focus.
//
// To ensure proper identity-based comparison, implementations should
// use pointer receivers for these methods, and Navigable instances should be
// passed to the Navigator as pointers.
type Navigable interface {
	Focused() bool
	Focus()
	Blur()
}

// Navigator manages focus between multiple navigable components using instance equality.
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

	n.Items[n.CurrentIndex].Blur()
	n.CurrentIndex = (n.CurrentIndex + 1) % len(n.Items)
	n.Items[n.CurrentIndex].Focus()
}

func (n *Navigator) Previous() {
	if len(n.Items) == 0 {
		return
	}

	n.Items[n.CurrentIndex].Blur()
	n.CurrentIndex = (n.CurrentIndex - 1 + len(n.Items)) % len(n.Items)
	n.Items[n.CurrentIndex].Focus()
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
		n.Items[0].Focus()
	}
}

// TODO: error for this.
func (n *Navigator) Remove(components ...Navigable) {
	for _, target := range components {
		for i, item := range n.Items {
			if item == target {
				// Unfocus if removing current
				if i == n.CurrentIndex {
					item.Blur()

					if len(n.Items) > 1 {
						n.CurrentIndex = (i - 1 + len(n.Items)) % len(n.Items)
						n.Items[n.CurrentIndex].Focus()
					} else {
						n.CurrentIndex = 0
					}
				} else if i < n.CurrentIndex {
					n.CurrentIndex--
				}

				// Remove item
				n.Items = append(n.Items[:i], n.Items[i+1:]...)

				// Break inner loop to process next target
				break
			}
		}
	}
}

func (n *Navigator) Replace(target Navigable, replacement ...Navigable) error {
	for i, item := range n.Items {
		if item == target {
			// Unfocus if replacing current
			wasFocused := (i == n.CurrentIndex)
			if wasFocused {
				item.Blur()
			}

			// Replace item with new components
			newItems := make([]Navigable, 0, len(n.Items)-1+len(replacement))
			newItems = append(newItems, n.Items[:i]...)
			newItems = append(newItems, replacement...)
			newItems = append(newItems, n.Items[i+1:]...)
			n.Items = newItems

			if len(n.Items) == 0 {
				n.CurrentIndex = 0

				return nil
			}

			if wasFocused {
				if len(replacement) > 0 {
					n.CurrentIndex = i
				} else {
					n.CurrentIndex = (i - 1 + len(n.Items)) % len(n.Items)
				}

				n.Items[n.CurrentIndex].Focus()
			} else if i < n.CurrentIndex {
				n.CurrentIndex += len(replacement) - 1
			}

			return nil
		}
	}

	return fmt.Errorf("navigable %v to replace not found", target)
}

func (n *Navigator) Reset() {
	n.Items = n.Items[:1]
	n.CurrentIndex = 0
}

func (n *Navigator) FocusNavigable(target Navigable) error {
	for i, item := range n.Items {
		if item == target {
			if i == n.CurrentIndex {
				return nil // already focused
			}

			n.Items[n.CurrentIndex].Blur() // unfocus current
			n.CurrentIndex = i
			n.Items[n.CurrentIndex].Focus() // focus target

			return nil
		}
	}

	return fmt.Errorf("navigable %v not found", target)
}
