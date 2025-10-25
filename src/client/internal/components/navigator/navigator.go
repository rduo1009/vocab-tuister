package navigator

type (
	AddNavigableMsg    struct{ Components []Navigable }
	RemoveNavigableMsg struct{ IDs []string }
)

// Navigable represents any component that can receive navigation focus.
type Navigable interface {
	SetFocused(bool)
	Focused() bool
	ID() string
}

// Navigator manages focus between multiple navigable components.
type Navigator struct {
	Items []Navigable
	Index int
}

func New(items []Navigable, index int) *Navigator {
	return &Navigator{
		Items: items,
		Index: index,
	}
}

func (n *Navigator) Next() {
	if len(n.Items) == 0 {
		return
	}
	n.Items[n.Index].SetFocused(false)
	n.Index = (n.Index + 1) % len(n.Items)
	n.Items[n.Index].SetFocused(true)
}

func (n *Navigator) Previous() {
	if len(n.Items) == 0 {
		return
	}
	n.Items[n.Index].SetFocused(false)
	n.Index = (n.Index - 1 + len(n.Items)) % len(n.Items)
	n.Items[n.Index].SetFocused(true)
}

func (n *Navigator) Current() Navigable {
	if len(n.Items) == 0 {
		return nil
	}
	return n.Items[n.Index]
}

func (n *Navigator) CurrentIndex() int {
	return n.Index
}

func (n *Navigator) Add(component Navigable) {
	n.Items = append(n.Items, component)
	// If this is the first item, set focus to it
	if len(n.Items) == 1 {
		n.Index = 0
		component.SetFocused(true)
	}
}

func (n *Navigator) Remove(id string) {
	for i, item := range n.Items {
		if item.ID() == id {
			// Unfocus if removing current
			if i == n.Index {
				item.SetFocused(false)
				if len(n.Items) > 1 {
					n.Index = (i - 1 + len(n.Items)) % len(n.Items)
					n.Items[n.Index].SetFocused(true)
				} else {
					n.Index = 0
				}
			} else if i < n.Index {
				n.Index--
			}

			// Remove item
			n.Items = append(n.Items[:i], n.Items[i+1:]...)
			return
		}
	}
}

func (n *Navigator) Reset() {
	n.Items = n.Items[:1]
	n.Index = 0
}
