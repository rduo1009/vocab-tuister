// Code generated by mkunion. DO NOT EDIT.
package schema

import (
	"encoding/json"
	"fmt"
	"github.com/widmogrod/mkunion/x/shared"
)

type SchemaVisitor interface {
	VisitNone(v *None) any
	VisitBool(v *Bool) any
	VisitNumber(v *Number) any
	VisitString(v *String) any
	VisitBinary(v *Binary) any
	VisitList(v *List) any
	VisitMap(v *Map) any
}

type Schema interface {
	AcceptSchema(g SchemaVisitor) any
}

var (
	_ Schema = (*None)(nil)
	_ Schema = (*Bool)(nil)
	_ Schema = (*Number)(nil)
	_ Schema = (*String)(nil)
	_ Schema = (*Binary)(nil)
	_ Schema = (*List)(nil)
	_ Schema = (*Map)(nil)
)

func (r *None) AcceptSchema(v SchemaVisitor) any   { return v.VisitNone(r) }
func (r *Bool) AcceptSchema(v SchemaVisitor) any   { return v.VisitBool(r) }
func (r *Number) AcceptSchema(v SchemaVisitor) any { return v.VisitNumber(r) }
func (r *String) AcceptSchema(v SchemaVisitor) any { return v.VisitString(r) }
func (r *Binary) AcceptSchema(v SchemaVisitor) any { return v.VisitBinary(r) }
func (r *List) AcceptSchema(v SchemaVisitor) any   { return v.VisitList(r) }
func (r *Map) AcceptSchema(v SchemaVisitor) any    { return v.VisitMap(r) }

func MatchSchemaR3[T0, T1, T2 any](
	x Schema,
	f1 func(x *None) (T0, T1, T2),
	f2 func(x *Bool) (T0, T1, T2),
	f3 func(x *Number) (T0, T1, T2),
	f4 func(x *String) (T0, T1, T2),
	f5 func(x *Binary) (T0, T1, T2),
	f6 func(x *List) (T0, T1, T2),
	f7 func(x *Map) (T0, T1, T2),
) (T0, T1, T2) {
	switch v := x.(type) {
	case *None:
		return f1(v)
	case *Bool:
		return f2(v)
	case *Number:
		return f3(v)
	case *String:
		return f4(v)
	case *Binary:
		return f5(v)
	case *List:
		return f6(v)
	case *Map:
		return f7(v)
	}
	var result1 T0
	var result2 T1
	var result3 T2
	return result1, result2, result3
}

func MatchSchemaR2[T0, T1 any](
	x Schema,
	f1 func(x *None) (T0, T1),
	f2 func(x *Bool) (T0, T1),
	f3 func(x *Number) (T0, T1),
	f4 func(x *String) (T0, T1),
	f5 func(x *Binary) (T0, T1),
	f6 func(x *List) (T0, T1),
	f7 func(x *Map) (T0, T1),
) (T0, T1) {
	switch v := x.(type) {
	case *None:
		return f1(v)
	case *Bool:
		return f2(v)
	case *Number:
		return f3(v)
	case *String:
		return f4(v)
	case *Binary:
		return f5(v)
	case *List:
		return f6(v)
	case *Map:
		return f7(v)
	}
	var result1 T0
	var result2 T1
	return result1, result2
}

func MatchSchemaR1[T0 any](
	x Schema,
	f1 func(x *None) T0,
	f2 func(x *Bool) T0,
	f3 func(x *Number) T0,
	f4 func(x *String) T0,
	f5 func(x *Binary) T0,
	f6 func(x *List) T0,
	f7 func(x *Map) T0,
) T0 {
	switch v := x.(type) {
	case *None:
		return f1(v)
	case *Bool:
		return f2(v)
	case *Number:
		return f3(v)
	case *String:
		return f4(v)
	case *Binary:
		return f5(v)
	case *List:
		return f6(v)
	case *Map:
		return f7(v)
	}
	var result1 T0
	return result1
}

func MatchSchemaR0(
	x Schema,
	f1 func(x *None),
	f2 func(x *Bool),
	f3 func(x *Number),
	f4 func(x *String),
	f5 func(x *Binary),
	f6 func(x *List),
	f7 func(x *Map),
) {
	switch v := x.(type) {
	case *None:
		f1(v)
	case *Bool:
		f2(v)
	case *Number:
		f3(v)
	case *String:
		f4(v)
	case *Binary:
		f5(v)
	case *List:
		f6(v)
	case *Map:
		f7(v)
	}
}
func init() {
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.Binary", BinaryFromJSON, BinaryToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.Bool", BoolFromJSON, BoolToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.List", ListFromJSON, ListToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.Map", MapFromJSON, MapToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.None", NoneFromJSON, NoneToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.Number", NumberFromJSON, NumberToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.Schema", SchemaFromJSON, SchemaToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/schema.String", StringFromJSON, StringToJSON)
}

type SchemaUnionJSON struct {
	Type   string          `json:"question_type,omitempty"`
	None   json.RawMessage `json:"schema.None,omitempty"`
	Bool   json.RawMessage `json:"schema.Bool,omitempty"`
	Number json.RawMessage `json:"schema.Number,omitempty"`
	String json.RawMessage `json:"schema.String,omitempty"`
	Binary json.RawMessage `json:"schema.Binary,omitempty"`
	List   json.RawMessage `json:"schema.List,omitempty"`
	Map    json.RawMessage `json:"schema.Map,omitempty"`
}

func SchemaFromJSON(x []byte) (Schema, error) {
	if x == nil || len(x) == 0 {
		return nil, nil
	}
	if string(x[:4]) == "null" {
		return nil, nil
	}
	var data SchemaUnionJSON
	err := json.Unmarshal(x, &data)
	if err != nil {
		return nil, fmt.Errorf("schema.SchemaFromJSON: %w", err)
	}

	switch data.Type {
	case "schema.None":
		return NoneFromJSON(data.None)
	case "schema.Bool":
		return BoolFromJSON(data.Bool)
	case "schema.Number":
		return NumberFromJSON(data.Number)
	case "schema.String":
		return StringFromJSON(data.String)
	case "schema.Binary":
		return BinaryFromJSON(data.Binary)
	case "schema.List":
		return ListFromJSON(data.List)
	case "schema.Map":
		return MapFromJSON(data.Map)
	}

	if data.None != nil {
		return NoneFromJSON(data.None)
	} else if data.Bool != nil {
		return BoolFromJSON(data.Bool)
	} else if data.Number != nil {
		return NumberFromJSON(data.Number)
	} else if data.String != nil {
		return StringFromJSON(data.String)
	} else if data.Binary != nil {
		return BinaryFromJSON(data.Binary)
	} else if data.List != nil {
		return ListFromJSON(data.List)
	} else if data.Map != nil {
		return MapFromJSON(data.Map)
	}
	return nil, fmt.Errorf("schema.SchemaFromJSON: unknown type: %s", data.Type)
}

func SchemaToJSON(x Schema) ([]byte, error) {
	if x == nil {
		return []byte(`null`), nil
	}
	return MatchSchemaR2(
		x,
		func(y *None) ([]byte, error) {
			body, err := NoneToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("schema.SchemaToJSON: %w", err)
			}
			return json.Marshal(SchemaUnionJSON{
				Type: "schema.None",
				None: body,
			})
		},
		func(y *Bool) ([]byte, error) {
			body, err := BoolToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("schema.SchemaToJSON: %w", err)
			}
			return json.Marshal(SchemaUnionJSON{
				Type: "schema.Bool",
				Bool: body,
			})
		},
		func(y *Number) ([]byte, error) {
			body, err := NumberToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("schema.SchemaToJSON: %w", err)
			}
			return json.Marshal(SchemaUnionJSON{
				Type:   "schema.Number",
				Number: body,
			})
		},
		func(y *String) ([]byte, error) {
			body, err := StringToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("schema.SchemaToJSON: %w", err)
			}
			return json.Marshal(SchemaUnionJSON{
				Type:   "schema.String",
				String: body,
			})
		},
		func(y *Binary) ([]byte, error) {
			body, err := BinaryToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("schema.SchemaToJSON: %w", err)
			}
			return json.Marshal(SchemaUnionJSON{
				Type:   "schema.Binary",
				Binary: body,
			})
		},
		func(y *List) ([]byte, error) {
			body, err := ListToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("schema.SchemaToJSON: %w", err)
			}
			return json.Marshal(SchemaUnionJSON{
				Type: "schema.List",
				List: body,
			})
		},
		func(y *Map) ([]byte, error) {
			body, err := MapToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("schema.SchemaToJSON: %w", err)
			}
			return json.Marshal(SchemaUnionJSON{
				Type: "schema.Map",
				Map:  body,
			})
		},
	)
}

func NoneFromJSON(x []byte) (*None, error) {
	result := new(None)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("schema.NoneFromJSON: %w", err)
	}
	return result, nil
}

func NoneToJSON(x *None) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*None)(nil)
	_ json.Marshaler   = (*None)(nil)
)

func (r *None) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONNone(*r)
}
func (r *None) _marshalJSONNone(x None) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schema: None._marshalJSONNone: struct; %w", err)
	}
	return result, nil
}
func (r *None) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONNone(data)
	if err != nil {
		return fmt.Errorf("schema: None.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *None) _unmarshalJSONNone(data []byte) (None, error) {
	result := None{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("schema: None._unmarshalJSONNone: native struct unwrap; %w", err)
	}
	return result, nil
}

func BoolFromJSON(x []byte) (*Bool, error) {
	result := new(Bool)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("schema.BoolFromJSON: %w", err)
	}
	return result, nil
}

func BoolToJSON(x *Bool) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Bool)(nil)
	_ json.Marshaler   = (*Bool)(nil)
)

func (r *Bool) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONBool(*r)
}
func (r *Bool) _marshalJSONBool(x Bool) ([]byte, error) {
	return r._marshalJSONbool(bool(x))
}
func (r *Bool) _marshalJSONbool(x bool) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("schema: Bool._marshalJSONbool:; %w", err)
	}
	return result, nil
}
func (r *Bool) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONBool(data)
	if err != nil {
		return fmt.Errorf("schema: Bool.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Bool) _unmarshalJSONBool(data []byte) (Bool, error) {
	var result Bool
	intermidiary, err := r._unmarshalJSONbool(data)
	if err != nil {
		return result, fmt.Errorf("schema: Bool._unmarshalJSONBool: alias; %w", err)
	}
	result = Bool(intermidiary)
	return result, nil
}
func (r *Bool) _unmarshalJSONbool(data []byte) (bool, error) {
	var result bool
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("schema: Bool._unmarshalJSONbool: native primitive unwrap; %w", err)
	}
	return result, nil
}

func NumberFromJSON(x []byte) (*Number, error) {
	result := new(Number)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("schema.NumberFromJSON: %w", err)
	}
	return result, nil
}

func NumberToJSON(x *Number) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Number)(nil)
	_ json.Marshaler   = (*Number)(nil)
)

func (r *Number) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONNumber(*r)
}
func (r *Number) _marshalJSONNumber(x Number) ([]byte, error) {
	return r._marshalJSONfloat64(float64(x))
}
func (r *Number) _marshalJSONfloat64(x float64) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("schema: Number._marshalJSONfloat64:; %w", err)
	}
	return result, nil
}
func (r *Number) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONNumber(data)
	if err != nil {
		return fmt.Errorf("schema: Number.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Number) _unmarshalJSONNumber(data []byte) (Number, error) {
	var result Number
	intermidiary, err := r._unmarshalJSONfloat64(data)
	if err != nil {
		return result, fmt.Errorf("schema: Number._unmarshalJSONNumber: alias; %w", err)
	}
	result = Number(intermidiary)
	return result, nil
}
func (r *Number) _unmarshalJSONfloat64(data []byte) (float64, error) {
	var result float64
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("schema: Number._unmarshalJSONfloat64: native primitive unwrap; %w", err)
	}
	return result, nil
}

func StringFromJSON(x []byte) (*String, error) {
	result := new(String)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("schema.StringFromJSON: %w", err)
	}
	return result, nil
}

func StringToJSON(x *String) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*String)(nil)
	_ json.Marshaler   = (*String)(nil)
)

func (r *String) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONString(*r)
}
func (r *String) _marshalJSONString(x String) ([]byte, error) {
	return r._marshalJSONstring(string(x))
}
func (r *String) _marshalJSONstring(x string) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("schema: String._marshalJSONstring:; %w", err)
	}
	return result, nil
}
func (r *String) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONString(data)
	if err != nil {
		return fmt.Errorf("schema: String.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *String) _unmarshalJSONString(data []byte) (String, error) {
	var result String
	intermidiary, err := r._unmarshalJSONstring(data)
	if err != nil {
		return result, fmt.Errorf("schema: String._unmarshalJSONString: alias; %w", err)
	}
	result = String(intermidiary)
	return result, nil
}
func (r *String) _unmarshalJSONstring(data []byte) (string, error) {
	var result string
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("schema: String._unmarshalJSONstring: native primitive unwrap; %w", err)
	}
	return result, nil
}

func BinaryFromJSON(x []byte) (*Binary, error) {
	result := new(Binary)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("schema.BinaryFromJSON: %w", err)
	}
	return result, nil
}

func BinaryToJSON(x *Binary) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Binary)(nil)
	_ json.Marshaler   = (*Binary)(nil)
)

func (r *Binary) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONBinary(*r)
}
func (r *Binary) _marshalJSONBinary(x Binary) ([]byte, error) {
	return r._marshalJSONSliceuint8([]uint8(x))
}
func (r *Binary) _marshalJSONSliceuint8(x []uint8) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("schema: Binary._marshalJSONSliceuint8:; %w", err)
	}
	return result, nil
}
func (r *Binary) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONBinary(data)
	if err != nil {
		return fmt.Errorf("schema: Binary.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Binary) _unmarshalJSONBinary(data []byte) (Binary, error) {
	var result Binary
	intermidiary, err := r._unmarshalJSONSliceuint8(data)
	if err != nil {
		return result, fmt.Errorf("schema: Binary._unmarshalJSONBinary: alias; %w", err)
	}
	result = Binary(intermidiary)
	return result, nil
}
func (r *Binary) _unmarshalJSONSliceuint8(data []byte) ([]uint8, error) {
	var result []uint8
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("schema: Binary._unmarshalJSONSliceuint8: native list unwrap; %w", err)
	}
	return result, nil
}

func ListFromJSON(x []byte) (*List, error) {
	result := new(List)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("schema.ListFromJSON: %w", err)
	}
	return result, nil
}

func ListToJSON(x *List) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*List)(nil)
	_ json.Marshaler   = (*List)(nil)
)

func (r *List) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONList(*r)
}
func (r *List) _marshalJSONList(x List) ([]byte, error) {
	return r._marshalJSONSliceSchema([]Schema(x))
}
func (r *List) _marshalJSONSliceSchema(x []Schema) ([]byte, error) {
	partial := make([]json.RawMessage, len(x))
	for i, v := range x {
		item, err := r._marshalJSONSchema(v)
		if err != nil {
			return nil, fmt.Errorf("schema: List._marshalJSONSliceSchema: at index %d; %w", i, err)
		}
		partial[i] = item
	}
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schema: List._marshalJSONSliceSchema:; %w", err)
	}
	return result, nil
}
func (r *List) _marshalJSONSchema(x Schema) ([]byte, error) {
	result, err := shared.JSONMarshal[Schema](x)
	if err != nil {
		return nil, fmt.Errorf("schema: List._marshalJSONSchema:; %w", err)
	}
	return result, nil
}
func (r *List) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONList(data)
	if err != nil {
		return fmt.Errorf("schema: List.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *List) _unmarshalJSONList(data []byte) (List, error) {
	var result List
	intermidiary, err := r._unmarshalJSONSliceSchema(data)
	if err != nil {
		return result, fmt.Errorf("schema: List._unmarshalJSONList: alias; %w", err)
	}
	result = List(intermidiary)
	return result, nil
}
func (r *List) _unmarshalJSONSliceSchema(data []byte) ([]Schema, error) {
	result := make([]Schema, 0)
	var partial []json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("schema: List._unmarshalJSONSliceSchema: native list unwrap; %w", err)
	}
	for i, v := range partial {
		item, err := r._unmarshalJSONSchema(v)
		if err != nil {
			return result, fmt.Errorf("schema: List._unmarshalJSONSliceSchema: at index %d; %w", i, err)
		}
		result = append(result, item)
	}
	return result, nil
}
func (r *List) _unmarshalJSONSchema(data []byte) (Schema, error) {
	result, err := shared.JSONUnmarshal[Schema](data)
	if err != nil {
		return result, fmt.Errorf("schema: List._unmarshalJSONSchema: native ref unwrap; %w", err)
	}
	return result, nil
}

func MapFromJSON(x []byte) (*Map, error) {
	result := new(Map)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("schema.MapFromJSON: %w", err)
	}
	return result, nil
}

func MapToJSON(x *Map) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Map)(nil)
	_ json.Marshaler   = (*Map)(nil)
)

func (r *Map) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONMap(*r)
}
func (r *Map) _marshalJSONMap(x Map) ([]byte, error) {
	return r._marshalJSONmapLb_string_bLSchema(map[string]Schema(x))
}
func (r *Map) _marshalJSONmapLb_string_bLSchema(x map[string]Schema) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	for k, v := range x {
		key := string(k)
		value, err := r._marshalJSONSchema(v)
		if err != nil {
			return nil, fmt.Errorf("schema: Map._marshalJSONmapLb_string_bLSchema: value; %w", err)
		}
		partial[string(key)] = value
	}
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schema: Map._marshalJSONmapLb_string_bLSchema:; %w", err)
	}
	return result, nil
}
func (r *Map) _marshalJSONstring(x string) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("schema: Map._marshalJSONstring:; %w", err)
	}
	return result, nil
}
func (r *Map) _marshalJSONSchema(x Schema) ([]byte, error) {
	result, err := shared.JSONMarshal[Schema](x)
	if err != nil {
		return nil, fmt.Errorf("schema: Map._marshalJSONSchema:; %w", err)
	}
	return result, nil
}
func (r *Map) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONMap(data)
	if err != nil {
		return fmt.Errorf("schema: Map.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Map) _unmarshalJSONMap(data []byte) (Map, error) {
	var result Map
	intermidiary, err := r._unmarshalJSONmapLb_string_bLSchema(data)
	if err != nil {
		return result, fmt.Errorf("schema: Map._unmarshalJSONMap: alias; %w", err)
	}
	result = Map(intermidiary)
	return result, nil
}
func (r *Map) _unmarshalJSONmapLb_string_bLSchema(data []byte) (map[string]Schema, error) {
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return nil, fmt.Errorf("schema: Map._unmarshalJSONmapLb_string_bLSchema: native map unwrap; %w", err)
	}
	result := make(map[string]Schema)
	for k, v := range partial {
		key := string(k)
		value, err := r._unmarshalJSONSchema(v)
		if err != nil {
			return nil, fmt.Errorf("schema: Map._unmarshalJSONmapLb_string_bLSchema: value; %w", err)
		}
		result[key] = value
	}
	return result, nil
}
func (r *Map) _unmarshalJSONstring(data []byte) (string, error) {
	var result string
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("schema: Map._unmarshalJSONstring: native primitive unwrap; %w", err)
	}
	return result, nil
}
func (r *Map) _unmarshalJSONSchema(data []byte) (Schema, error) {
	result, err := shared.JSONUnmarshal[Schema](data)
	if err != nil {
		return result, fmt.Errorf("schema: Map._unmarshalJSONSchema: native ref unwrap; %w", err)
	}
	return result, nil
}
