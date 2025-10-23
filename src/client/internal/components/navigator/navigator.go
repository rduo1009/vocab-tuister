package navigator

// Navigable represents any component that can receive navigation focus.
type Navigable interface {
	SetFocused(bool)
	Focused() bool
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
