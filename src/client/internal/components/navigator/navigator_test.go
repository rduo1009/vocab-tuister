package navigator_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
)

type mockNavigable struct {
	mock.Mock
}

func (m *mockNavigable) Focused() bool {
	args := m.Called()
	return args.Bool(0)
}

func (m *mockNavigable) Focus() {
	m.Called()
}

func (m *mockNavigable) Blur() {
	m.Called()
}

func TestNavigator_New(t *testing.T) {
	n1 := &mockNavigable{}
	n2 := &mockNavigable{}
	items := []navigator.Navigable{n1, n2}
	n := navigator.New(items, 1)

	assert.Equal(t, items, n.Items)
	assert.Equal(t, 1, n.CurrentIndex)
	assert.Equal(t, n2, n.Current())
}

func TestNavigator_NextPrevious(t *testing.T) {
	n1 := &mockNavigable{}
	n2 := &mockNavigable{}
	n3 := &mockNavigable{}
	n := navigator.New([]navigator.Navigable{n1, n2, n3}, 0)

	// Setup expectations
	n1.On("Blur")
	n2.On("Focus")
	n2.On("Blur")
	n3.On("Focus")
	n3.On("Blur")
	n1.On("Focus")

	n.Next()
	assert.Equal(t, 1, n.CurrentIndex)

	n.Next()
	assert.Equal(t, 2, n.CurrentIndex)

	// Wrap Next
	n.Next()
	assert.Equal(t, 0, n.CurrentIndex)

	// Wrap Previous
	n.Previous()
	assert.Equal(t, 2, n.CurrentIndex)

	n.Previous()
	assert.Equal(t, 1, n.CurrentIndex)

	n1.AssertExpectations(t)
	n2.AssertExpectations(t)
	n3.AssertExpectations(t)
}

func TestNavigator_Add(t *testing.T) {
	t.Run("add to existing", func(t *testing.T) {
		n1 := &mockNavigable{}
		n2 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1}, 0)

		n.Add(n2)
		assert.Equal(t, 2, len(n.Items))
		assert.Equal(t, n2, n.Items[1])
	})

	t.Run("add to empty", func(t *testing.T) {
		n := navigator.New(nil, 0)
		n1 := &mockNavigable{}
		n1.On("Focus")

		n.Add(n1)
		assert.Equal(t, 1, len(n.Items))
		assert.Equal(t, 0, n.CurrentIndex)
		n1.AssertExpectations(t)
	})
}

func TestNavigator_Remove(t *testing.T) {
	t.Run("remove non-current", func(t *testing.T) {
		n1 := &mockNavigable{}
		n2 := &mockNavigable{}
		n3 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1, n2, n3}, 1)

		err := n.Remove(n3)
		require.NoError(t, err)
		assert.Equal(t, 2, len(n.Items))
		assert.Equal(t, 1, n.CurrentIndex)

		err = n.Remove(n1)
		require.NoError(t, err)
		assert.Equal(t, 1, len(n.Items))
		assert.Equal(t, 0, n.CurrentIndex)
		assert.Equal(t, n2, n.Current())
	})

	t.Run("remove current with others", func(t *testing.T) {
		n1 := &mockNavigable{}
		n2 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1, n2}, 1)

		n2.On("Blur")
		n1.On("Focus")

		err := n.Remove(n2)
		require.NoError(t, err)
		assert.Equal(t, 1, len(n.Items))
		assert.Equal(t, 0, n.CurrentIndex)
		n1.AssertExpectations(t)
		n2.AssertExpectations(t)
	})

	t.Run("remove last item", func(t *testing.T) {
		n1 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1}, 0)

		n1.On("Blur")

		err := n.Remove(n1)
		require.NoError(t, err)
		assert.Equal(t, 0, len(n.Items))
		n1.AssertExpectations(t)
	})

	t.Run("remove not found", func(t *testing.T) {
		n1 := &mockNavigable{}
		n2 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1}, 0)

		err := n.Remove(n2)
		assert.Error(t, err)
	})
}

func TestNavigator_Replace(t *testing.T) {
	t.Run("replace current with multiple", func(t *testing.T) {
		n1 := &mockNavigable{}
		n2 := &mockNavigable{}
		n3 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1}, 0)

		n1.On("Blur")
		n2.On("Focus")

		err := n.Replace(n1, n2, n3)
		require.NoError(t, err)

		assert.Equal(t, 2, len(n.Items))
		assert.Equal(t, 0, n.CurrentIndex)
		n1.AssertExpectations(t)
		n2.AssertExpectations(t)
	})

	t.Run("replace non-current before index", func(t *testing.T) {
		n1 := &mockNavigable{}
		n2 := &mockNavigable{}
		n3 := &mockNavigable{}
		n4 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1, n2}, 1)

		err := n.Replace(n1, n3, n4)
		require.NoError(t, err)

		assert.Equal(t, 3, len(n.Items))
		assert.Equal(t, 2, n.CurrentIndex)
		assert.Equal(t, n2, n.Current())
	})

	t.Run("replace not found", func(t *testing.T) {
		n1 := &mockNavigable{}
		n2 := &mockNavigable{}
		n := navigator.New([]navigator.Navigable{n1}, 0)

		err := n.Replace(n2, n1)
		assert.Error(t, err)
	})
}

func TestNavigator_Reset(t *testing.T) {
	n1 := &mockNavigable{}
	n2 := &mockNavigable{}
	n := navigator.New([]navigator.Navigable{n1, n2}, 1)

	n2.On("Blur")
	n1.On("Focus")
	n1.On("Blur")

	n.Reset()
	assert.Equal(t, 1, len(n.Items))
	assert.Equal(t, 0, n.CurrentIndex)
	assert.Equal(t, n1, n.Current())

	n1.AssertExpectations(t)
	n2.AssertExpectations(t)
}

func TestNavigator_FocusNavigable(t *testing.T) {
	n1 := &mockNavigable{}
	n2 := &mockNavigable{}
	n := navigator.New([]navigator.Navigable{n1, n2}, 0)

	n1.On("Blur")
	n2.On("Focus")

	err := n.FocusNavigable(n2)
	require.NoError(t, err)
	assert.Equal(t, 1, n.CurrentIndex)

	err = n.FocusNavigable(&mockNavigable{})
	assert.Error(t, err)

	n1.AssertExpectations(t)
	n2.AssertExpectations(t)
}
