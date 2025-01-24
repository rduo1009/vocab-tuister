# x/schema - Golang recursive schema
Library allows to write code that work with any type of schemas.
Regardless if those are JSON, XML, YAML, or golang structs.

Most benefits
- Union types can be deserialized into interface field

## How to convert between json <-> go
```go
data := `{"name": "John", "cars": [{"name":"Ford"}]}`
schema := schema.FromJSON(data)
nativego, err := schema.ToGo(schema)

expected := map[string]any{
    "name": "John",
    "cars": []any{
        map[string]any{
            "name": "Ford",
        },
    },
}
assert.Equal(t, expected, nativego)
```

## How to convert schema into named golang struct?
This example shows how to convert only part of schema to golang struct.
List of cars will have type `Car` when parent `Person` object will be `map[string]any`.
```go
type Car struct {
    Name string
}
nativego := schema.MustToGo(schema, WithOnlyTheseRules(
	WhenPath([]string{"cars", "[*]"}, UseStruct(Car{}))))

expected := map[string]any{
    "name": "John",
    "cars": []any{
        Car{
            Name: "Ford",
        },
    },
}
assert.Equal(t, expected, nativego)
```

## How to define custom serialization and deserilization?
Currently, ser-deser operations are available on maps.
This is current design decision, it might change in the future.

```go
type Car struct {
    Name string
}

// make sure to Car implements schema.Marshaler and schema.Unmarshaler
var (
	_ schema.Marshaler = (*Car)(nil)
    _ schema.Unmarshaler = (*Car)(nil)
)

func (c *Car) MarshalSchema() (schema.*Map, error) {
    return schema.MkMap(map[string]schema.Schema{
        "name": schema.MkString(c.Name),
    }), nil
}

func (c *Car) UnmarshalSchema(x schema.*Map) error {
    for _, field := range x.Field {
        switch key {
        case "name":
            c.Name = s.MustToString()
        default:
            return fmt.Errorf("unknown key %s", key)
        }
    }
	
    return nil
}
```

### How to convert well defined types from external packages?
```go
type Car struct {
    Name string
    LastDriven time.Time
}

// Register conversion from time.Time to schema.String
schema.RegisterWellDefinedTypesConversion[time.Time](
  func(x time.Time) Schema {
      return MkString(x.Format(time.RFC3339Nano))
  },
  func(x Schema) time.Time {
      if v, ok := x.(*String); ok {
          t, _ := time.Parse(time.RFC3339Nano, string(*v))
          return t
      }

      panic("invalid type")
  },
)

// Then you can translate schema between back and forth without worrying about time.Time
schema := FromGo(data)
result, err := ToGoG[ExternalPackageStruct](schema)
assert.NoError(t, err)
assert.Equal(t, data, result)
```

## Roadmap
### V0.1.0
- [x] Json <-> Schema <-> Go (with structs mapping)
- [x] Write test with wrong type conversions
- [x] Value are split into Number(Int, Float), String, Bool, and Null
- [x] Default schema registry + mkunion make union serialization/deserialization work transperently
- [x] Support pointers *string, etc.
- [x] Support DynamoDB (FromDynamoDB, ToDynamoDB)
- [x] Support for pointer to types like *string, *int, etc.
- [x] Support for relative paths like `WhenPath([]string{"*", "ListOfCars", "Car"}, UseStruct(Car{}))`. 
      Absolute paths are without `*` at the beginning.
 
### V0.2.x
- [x] Support options for `ToGo` & `FromGo` like `WithOnlyTheseRules`, `WithExtraRules`, `WithDefaultMapDef`, etc. 
      Gives better control on how schema is converted to golang.
      It's especially important from security reasons, whey you want to allow rules only whitelisted rules, for user generated json input.
- [x] Schema support interface for custom type-setters, that don't require reflection, and mkunion can leverage them. Use `UseTypeDef` eg. `WhenPath([]string{}, UseTypeDef(&someTypeDef{})),`
- [x] Support for how union names should be expressed in schema `WithUnionFormatter(func(t reflect.Type) string)`

### V0.3.x
- [x] schema.Compare method to compare two schemas

### V0.4.x
- [x] Support for Binary type
- [x] Add missing function for MkBinary, MkFloat, MkNone

### V0.5.x
- [x] `schema.UnwrapDynamoDB` takes DynamoDB specific nesting and removes it.
- [x] Eliminate data races in `*UnionVariants[A] -> MapDefFor` & `UseUnionFormatter` data race
- [x] Introduce `ToGoG[T any]` function, that makes ToGo with type assertion and tries to convert to T
- [x] Rename `schema.As` to `schema.AsDefault` and make `schema.As` as variant that returns false, if type is not supported

### V0.6.x
- [x] Support serialization of `schema.Marchaler` to `schema.Unmarshaller`, that can dramatically improve performance in some cases.
      Limitation of current implementation is that it works only on *Map, and don't allow custom ser-deser on other types.
      It's not hard decision. It's just that I don't have use case for other types yet.

### V0.7.x
- [x] schema.Schema is now serializable and deserilizable

### V0.8.x
- [x] `schema` use `x/shape` and native types to represent variants like Map and List and Bytes
- [x] schema.Schema is refactored to leverage simpler types thanks to `x/shape` library
- [x] schema.ToJSON and schema.FromJSON are removed and replaced by `mkunion` defaults

### V0.11.x
- [ ] `schema` becomes `data`
- [ ] data.FromGo and data.ToGo works only on primitive values
- [ ] data.FromStruct and data.ToStruct works only on structs and reflection
- [ ] data.FromDynamoDB and data.ToDynamoDB refactored