# Welcome to MkUnion
[![Go Reference](https://pkg.go.dev/badge/github.com/widmogrod/mkunion.svg)](https://pkg.go.dev/github.com/widmogrod/mkunion)
[![Go Report Card](https://goreportcard.com/badge/github.com/widmogrod/mkunion)](https://goreportcard.com/report/github.com/widmogrod/mkunion)
[![codecov](https://codecov.io/gh/widmogrod/mkunion/branch/main/graph/badge.svg?token=3Z3Z3Z3Z3Z)](https://codecov.io/gh/widmogrod/mkunion)

> [!NOTE]
> This is a vendored copy of mkunion from https://github.com/widmogrod/mkunion.
> Dev files, documentation, testing files and unused code have been removed.
> Some changes have been made to fit its usage in vocab-tuister.

## About
Strongly typed **union type** in golang with generics*.

* with exhaustive _pattern matching_ support
* with _json marshalling_ including generics
* and as a bonus, can generate compatible typescript types for end-to-end type safety in your application

## Why
Historically in languages without union types like golang, unions were solved either by using Visitor pattern, or using `iota` and `switch` statement, or other workarounds.

Visitor pattern requires a lot of boiler plate code and hand crafting of the `Accept` method for each type in the union.
`iota` and `switch` statement is not type safe and can lead to runtime errors, especially when new type is added and not all `case` statements are updated.

On top of that, any data marshalling like to/from JSON requires additional, hand crafted code, to make it work.

MkUnion solves all of those problems, by generating opinionated and strongly typed meaningful code for you.

## Example

```go title="example/vehicle.go"
package example

//go:generate mkunion

// union declaration
//go:tag mkunion:"Vehicle"
type (
	Car struct {
		Color  string
		Wheels int
	}
	Plane struct {
		Color   string
		Engines int
	}
	Boat struct {
		Color      string
		Propellers int
	}
)

func CalculateFuelUsage(v Vehicle) int {
	// example of pattern matching over Vehicle union type
	return MatchVehicleR1(
		v,
		func(x *Car) int {
			return x.Wheels * 2
		},
		func(x *Plane) int {
			return x.Engines * 10
		},
		func(x *Boat) int {
			return x.Propellers * 5
		},
	)
}

func ExampleToJSON() {
    var vehicle Vehicle = &Car{
        Color:  "black",
        Wheels: 4,
    }
    result, _ := shared.JSONMarshal(vehicle)
    fmt.Println(string(result))
    // Output: {"question_type":"example.Car","example.Car":{"Color":"black","Wheels":4}}
}

func ExampleFromJSON() {
	input := []byte(`{"question_type":"example.Car","example.Car":{"Color":"black","Wheels":4}}`)
	vehicle, _ := shared.JSONUnmarshal[Vehicle](input)
	fmt.Printf("%#v", vehicle)
	// Output: &example.Car{Color:"black", Wheels:4}
}
```


## Next

- Read [getting started](https://widmogrod.github.io/mkunion/getting_started/)  to learn more.