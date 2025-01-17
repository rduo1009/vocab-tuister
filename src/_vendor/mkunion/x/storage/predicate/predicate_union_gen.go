// Code generated by mkunion. DO NOT EDIT.
package predicate

import (
	"encoding/json"
	"fmt"
	"github.com/widmogrod/mkunion/x/schema"
	"github.com/widmogrod/mkunion/x/shared"
)

type BindableVisitor interface {
	VisitBindValue(v *BindValue) any
	VisitLiteral(v *Literal) any
	VisitLocatable(v *Locatable) any
}

type Bindable interface {
	AcceptBindable(g BindableVisitor) any
}

var (
	_ Bindable = (*BindValue)(nil)
	_ Bindable = (*Literal)(nil)
	_ Bindable = (*Locatable)(nil)
)

func (r *BindValue) AcceptBindable(v BindableVisitor) any { return v.VisitBindValue(r) }
func (r *Literal) AcceptBindable(v BindableVisitor) any   { return v.VisitLiteral(r) }
func (r *Locatable) AcceptBindable(v BindableVisitor) any { return v.VisitLocatable(r) }

func MatchBindableR3[T0, T1, T2 any](
	x Bindable,
	f1 func(x *BindValue) (T0, T1, T2),
	f2 func(x *Literal) (T0, T1, T2),
	f3 func(x *Locatable) (T0, T1, T2),
) (T0, T1, T2) {
	switch v := x.(type) {
	case *BindValue:
		return f1(v)
	case *Literal:
		return f2(v)
	case *Locatable:
		return f3(v)
	}
	var result1 T0
	var result2 T1
	var result3 T2
	return result1, result2, result3
}

func MatchBindableR2[T0, T1 any](
	x Bindable,
	f1 func(x *BindValue) (T0, T1),
	f2 func(x *Literal) (T0, T1),
	f3 func(x *Locatable) (T0, T1),
) (T0, T1) {
	switch v := x.(type) {
	case *BindValue:
		return f1(v)
	case *Literal:
		return f2(v)
	case *Locatable:
		return f3(v)
	}
	var result1 T0
	var result2 T1
	return result1, result2
}

func MatchBindableR1[T0 any](
	x Bindable,
	f1 func(x *BindValue) T0,
	f2 func(x *Literal) T0,
	f3 func(x *Locatable) T0,
) T0 {
	switch v := x.(type) {
	case *BindValue:
		return f1(v)
	case *Literal:
		return f2(v)
	case *Locatable:
		return f3(v)
	}
	var result1 T0
	return result1
}

func MatchBindableR0(
	x Bindable,
	f1 func(x *BindValue),
	f2 func(x *Literal),
	f3 func(x *Locatable),
) {
	switch v := x.(type) {
	case *BindValue:
		f1(v)
	case *Literal:
		f2(v)
	case *Locatable:
		f3(v)
	}
}
func init() {
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.BindValue", BindValueFromJSON, BindValueToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.Bindable", BindableFromJSON, BindableToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.Literal", LiteralFromJSON, LiteralToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.Locatable", LocatableFromJSON, LocatableToJSON)
}

type BindableUnionJSON struct {
	Type      string          `json:"question_type,omitempty"`
	BindValue json.RawMessage `json:"predicate.BindValue,omitempty"`
	Literal   json.RawMessage `json:"predicate.Literal,omitempty"`
	Locatable json.RawMessage `json:"predicate.Locatable,omitempty"`
}

func BindableFromJSON(x []byte) (Bindable, error) {
	if x == nil || len(x) == 0 {
		return nil, nil
	}
	if string(x[:4]) == "null" {
		return nil, nil
	}
	var data BindableUnionJSON
	err := json.Unmarshal(x, &data)
	if err != nil {
		return nil, fmt.Errorf("predicate.BindableFromJSON: %w", err)
	}

	switch data.Type {
	case "predicate.BindValue":
		return BindValueFromJSON(data.BindValue)
	case "predicate.Literal":
		return LiteralFromJSON(data.Literal)
	case "predicate.Locatable":
		return LocatableFromJSON(data.Locatable)
	}

	if data.BindValue != nil {
		return BindValueFromJSON(data.BindValue)
	} else if data.Literal != nil {
		return LiteralFromJSON(data.Literal)
	} else if data.Locatable != nil {
		return LocatableFromJSON(data.Locatable)
	}
	return nil, fmt.Errorf("predicate.BindableFromJSON: unknown type: %s", data.Type)
}

func BindableToJSON(x Bindable) ([]byte, error) {
	if x == nil {
		return []byte(`null`), nil
	}
	return MatchBindableR2(
		x,
		func(y *BindValue) ([]byte, error) {
			body, err := BindValueToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("predicate.BindableToJSON: %w", err)
			}
			return json.Marshal(BindableUnionJSON{
				Type:      "predicate.BindValue",
				BindValue: body,
			})
		},
		func(y *Literal) ([]byte, error) {
			body, err := LiteralToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("predicate.BindableToJSON: %w", err)
			}
			return json.Marshal(BindableUnionJSON{
				Type:    "predicate.Literal",
				Literal: body,
			})
		},
		func(y *Locatable) ([]byte, error) {
			body, err := LocatableToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("predicate.BindableToJSON: %w", err)
			}
			return json.Marshal(BindableUnionJSON{
				Type:      "predicate.Locatable",
				Locatable: body,
			})
		},
	)
}

func BindValueFromJSON(x []byte) (*BindValue, error) {
	result := new(BindValue)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("predicate.BindValueFromJSON: %w", err)
	}
	return result, nil
}

func BindValueToJSON(x *BindValue) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*BindValue)(nil)
	_ json.Marshaler   = (*BindValue)(nil)
)

func (r *BindValue) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONBindValue(*r)
}
func (r *BindValue) _marshalJSONBindValue(x BindValue) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldBindName []byte
	fieldBindName, err = r._marshalJSONBindName(x.BindName)
	if err != nil {
		return nil, fmt.Errorf("predicate: BindValue._marshalJSONBindValue: field name BindName; %w", err)
	}
	partial["BindName"] = fieldBindName
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: BindValue._marshalJSONBindValue: struct; %w", err)
	}
	return result, nil
}
func (r *BindValue) _marshalJSONBindName(x BindName) ([]byte, error) {
	result, err := shared.JSONMarshal[BindName](x)
	if err != nil {
		return nil, fmt.Errorf("predicate: BindValue._marshalJSONBindName:; %w", err)
	}
	return result, nil
}
func (r *BindValue) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONBindValue(data)
	if err != nil {
		return fmt.Errorf("predicate: BindValue.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *BindValue) _unmarshalJSONBindValue(data []byte) (BindValue, error) {
	result := BindValue{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: BindValue._unmarshalJSONBindValue: native struct unwrap; %w", err)
	}
	if fieldBindName, ok := partial["BindName"]; ok {
		result.BindName, err = r._unmarshalJSONBindName(fieldBindName)
		if err != nil {
			return result, fmt.Errorf("predicate: BindValue._unmarshalJSONBindValue: field BindName; %w", err)
		}
	}
	return result, nil
}
func (r *BindValue) _unmarshalJSONBindName(data []byte) (BindName, error) {
	result, err := shared.JSONUnmarshal[BindName](data)
	if err != nil {
		return result, fmt.Errorf("predicate: BindValue._unmarshalJSONBindName: native ref unwrap; %w", err)
	}
	return result, nil
}

func LiteralFromJSON(x []byte) (*Literal, error) {
	result := new(Literal)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("predicate.LiteralFromJSON: %w", err)
	}
	return result, nil
}

func LiteralToJSON(x *Literal) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Literal)(nil)
	_ json.Marshaler   = (*Literal)(nil)
)

func (r *Literal) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONLiteral(*r)
}
func (r *Literal) _marshalJSONLiteral(x Literal) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldValue []byte
	fieldValue, err = r._marshalJSONschema_Schema(x.Value)
	if err != nil {
		return nil, fmt.Errorf("predicate: Literal._marshalJSONLiteral: field name Value; %w", err)
	}
	partial["Value"] = fieldValue
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: Literal._marshalJSONLiteral: struct; %w", err)
	}
	return result, nil
}
func (r *Literal) _marshalJSONschema_Schema(x schema.Schema) ([]byte, error) {
	result, err := shared.JSONMarshal[schema.Schema](x)
	if err != nil {
		return nil, fmt.Errorf("predicate: Literal._marshalJSONschema_Schema:; %w", err)
	}
	return result, nil
}
func (r *Literal) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONLiteral(data)
	if err != nil {
		return fmt.Errorf("predicate: Literal.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Literal) _unmarshalJSONLiteral(data []byte) (Literal, error) {
	result := Literal{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: Literal._unmarshalJSONLiteral: native struct unwrap; %w", err)
	}
	if fieldValue, ok := partial["Value"]; ok {
		result.Value, err = r._unmarshalJSONschema_Schema(fieldValue)
		if err != nil {
			return result, fmt.Errorf("predicate: Literal._unmarshalJSONLiteral: field Value; %w", err)
		}
	}
	return result, nil
}
func (r *Literal) _unmarshalJSONschema_Schema(data []byte) (schema.Schema, error) {
	result, err := shared.JSONUnmarshal[schema.Schema](data)
	if err != nil {
		return result, fmt.Errorf("predicate: Literal._unmarshalJSONschema_Schema: native ref unwrap; %w", err)
	}
	return result, nil
}

func LocatableFromJSON(x []byte) (*Locatable, error) {
	result := new(Locatable)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("predicate.LocatableFromJSON: %w", err)
	}
	return result, nil
}

func LocatableToJSON(x *Locatable) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Locatable)(nil)
	_ json.Marshaler   = (*Locatable)(nil)
)

func (r *Locatable) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONLocatable(*r)
}
func (r *Locatable) _marshalJSONLocatable(x Locatable) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldLocation []byte
	fieldLocation, err = r._marshalJSONstring(x.Location)
	if err != nil {
		return nil, fmt.Errorf("predicate: Locatable._marshalJSONLocatable: field name Location; %w", err)
	}
	partial["Location"] = fieldLocation
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: Locatable._marshalJSONLocatable: struct; %w", err)
	}
	return result, nil
}
func (r *Locatable) _marshalJSONstring(x string) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("predicate: Locatable._marshalJSONstring:; %w", err)
	}
	return result, nil
}
func (r *Locatable) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONLocatable(data)
	if err != nil {
		return fmt.Errorf("predicate: Locatable.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Locatable) _unmarshalJSONLocatable(data []byte) (Locatable, error) {
	result := Locatable{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: Locatable._unmarshalJSONLocatable: native struct unwrap; %w", err)
	}
	if fieldLocation, ok := partial["Location"]; ok {
		result.Location, err = r._unmarshalJSONstring(fieldLocation)
		if err != nil {
			return result, fmt.Errorf("predicate: Locatable._unmarshalJSONLocatable: field Location; %w", err)
		}
	}
	return result, nil
}
func (r *Locatable) _unmarshalJSONstring(data []byte) (string, error) {
	var result string
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("predicate: Locatable._unmarshalJSONstring: native primitive unwrap; %w", err)
	}
	return result, nil
}

type PredicateVisitor interface {
	VisitAnd(v *And) any
	VisitOr(v *Or) any
	VisitNot(v *Not) any
	VisitCompare(v *Compare) any
}

type Predicate interface {
	AcceptPredicate(g PredicateVisitor) any
}

var (
	_ Predicate = (*And)(nil)
	_ Predicate = (*Or)(nil)
	_ Predicate = (*Not)(nil)
	_ Predicate = (*Compare)(nil)
)

func (r *And) AcceptPredicate(v PredicateVisitor) any     { return v.VisitAnd(r) }
func (r *Or) AcceptPredicate(v PredicateVisitor) any      { return v.VisitOr(r) }
func (r *Not) AcceptPredicate(v PredicateVisitor) any     { return v.VisitNot(r) }
func (r *Compare) AcceptPredicate(v PredicateVisitor) any { return v.VisitCompare(r) }

func MatchPredicateR3[T0, T1, T2 any](
	x Predicate,
	f1 func(x *And) (T0, T1, T2),
	f2 func(x *Or) (T0, T1, T2),
	f3 func(x *Not) (T0, T1, T2),
	f4 func(x *Compare) (T0, T1, T2),
) (T0, T1, T2) {
	switch v := x.(type) {
	case *And:
		return f1(v)
	case *Or:
		return f2(v)
	case *Not:
		return f3(v)
	case *Compare:
		return f4(v)
	}
	var result1 T0
	var result2 T1
	var result3 T2
	return result1, result2, result3
}

func MatchPredicateR2[T0, T1 any](
	x Predicate,
	f1 func(x *And) (T0, T1),
	f2 func(x *Or) (T0, T1),
	f3 func(x *Not) (T0, T1),
	f4 func(x *Compare) (T0, T1),
) (T0, T1) {
	switch v := x.(type) {
	case *And:
		return f1(v)
	case *Or:
		return f2(v)
	case *Not:
		return f3(v)
	case *Compare:
		return f4(v)
	}
	var result1 T0
	var result2 T1
	return result1, result2
}

func MatchPredicateR1[T0 any](
	x Predicate,
	f1 func(x *And) T0,
	f2 func(x *Or) T0,
	f3 func(x *Not) T0,
	f4 func(x *Compare) T0,
) T0 {
	switch v := x.(type) {
	case *And:
		return f1(v)
	case *Or:
		return f2(v)
	case *Not:
		return f3(v)
	case *Compare:
		return f4(v)
	}
	var result1 T0
	return result1
}

func MatchPredicateR0(
	x Predicate,
	f1 func(x *And),
	f2 func(x *Or),
	f3 func(x *Not),
	f4 func(x *Compare),
) {
	switch v := x.(type) {
	case *And:
		f1(v)
	case *Or:
		f2(v)
	case *Not:
		f3(v)
	case *Compare:
		f4(v)
	}
}
func init() {
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.And", AndFromJSON, AndToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.Compare", CompareFromJSON, CompareToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.Not", NotFromJSON, NotToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.Or", OrFromJSON, OrToJSON)
	shared.JSONMarshallerRegister("github.com/widmogrod/mkunion/x/storage/predicate.Predicate", PredicateFromJSON, PredicateToJSON)
}

type PredicateUnionJSON struct {
	Type    string          `json:"question_type,omitempty"`
	And     json.RawMessage `json:"predicate.And,omitempty"`
	Or      json.RawMessage `json:"predicate.Or,omitempty"`
	Not     json.RawMessage `json:"predicate.Not,omitempty"`
	Compare json.RawMessage `json:"predicate.Compare,omitempty"`
}

func PredicateFromJSON(x []byte) (Predicate, error) {
	if x == nil || len(x) == 0 {
		return nil, nil
	}
	if string(x[:4]) == "null" {
		return nil, nil
	}
	var data PredicateUnionJSON
	err := json.Unmarshal(x, &data)
	if err != nil {
		return nil, fmt.Errorf("predicate.PredicateFromJSON: %w", err)
	}

	switch data.Type {
	case "predicate.And":
		return AndFromJSON(data.And)
	case "predicate.Or":
		return OrFromJSON(data.Or)
	case "predicate.Not":
		return NotFromJSON(data.Not)
	case "predicate.Compare":
		return CompareFromJSON(data.Compare)
	}

	if data.And != nil {
		return AndFromJSON(data.And)
	} else if data.Or != nil {
		return OrFromJSON(data.Or)
	} else if data.Not != nil {
		return NotFromJSON(data.Not)
	} else if data.Compare != nil {
		return CompareFromJSON(data.Compare)
	}
	return nil, fmt.Errorf("predicate.PredicateFromJSON: unknown type: %s", data.Type)
}

func PredicateToJSON(x Predicate) ([]byte, error) {
	if x == nil {
		return []byte(`null`), nil
	}
	return MatchPredicateR2(
		x,
		func(y *And) ([]byte, error) {
			body, err := AndToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("predicate.PredicateToJSON: %w", err)
			}
			return json.Marshal(PredicateUnionJSON{
				Type: "predicate.And",
				And:  body,
			})
		},
		func(y *Or) ([]byte, error) {
			body, err := OrToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("predicate.PredicateToJSON: %w", err)
			}
			return json.Marshal(PredicateUnionJSON{
				Type: "predicate.Or",
				Or:   body,
			})
		},
		func(y *Not) ([]byte, error) {
			body, err := NotToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("predicate.PredicateToJSON: %w", err)
			}
			return json.Marshal(PredicateUnionJSON{
				Type: "predicate.Not",
				Not:  body,
			})
		},
		func(y *Compare) ([]byte, error) {
			body, err := CompareToJSON(y)
			if err != nil {
				return nil, fmt.Errorf("predicate.PredicateToJSON: %w", err)
			}
			return json.Marshal(PredicateUnionJSON{
				Type:    "predicate.Compare",
				Compare: body,
			})
		},
	)
}

func AndFromJSON(x []byte) (*And, error) {
	result := new(And)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("predicate.AndFromJSON: %w", err)
	}
	return result, nil
}

func AndToJSON(x *And) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*And)(nil)
	_ json.Marshaler   = (*And)(nil)
)

func (r *And) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONAnd(*r)
}
func (r *And) _marshalJSONAnd(x And) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldL []byte
	fieldL, err = r._marshalJSONSlicePredicate(x.L)
	if err != nil {
		return nil, fmt.Errorf("predicate: And._marshalJSONAnd: field name L; %w", err)
	}
	partial["L"] = fieldL
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: And._marshalJSONAnd: struct; %w", err)
	}
	return result, nil
}
func (r *And) _marshalJSONSlicePredicate(x []Predicate) ([]byte, error) {
	partial := make([]json.RawMessage, len(x))
	for i, v := range x {
		item, err := r._marshalJSONPredicate(v)
		if err != nil {
			return nil, fmt.Errorf("predicate: And._marshalJSONSlicePredicate: at index %d; %w", i, err)
		}
		partial[i] = item
	}
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: And._marshalJSONSlicePredicate:; %w", err)
	}
	return result, nil
}
func (r *And) _marshalJSONPredicate(x Predicate) ([]byte, error) {
	result, err := shared.JSONMarshal[Predicate](x)
	if err != nil {
		return nil, fmt.Errorf("predicate: And._marshalJSONPredicate:; %w", err)
	}
	return result, nil
}
func (r *And) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONAnd(data)
	if err != nil {
		return fmt.Errorf("predicate: And.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *And) _unmarshalJSONAnd(data []byte) (And, error) {
	result := And{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: And._unmarshalJSONAnd: native struct unwrap; %w", err)
	}
	if fieldL, ok := partial["L"]; ok {
		result.L, err = r._unmarshalJSONSlicePredicate(fieldL)
		if err != nil {
			return result, fmt.Errorf("predicate: And._unmarshalJSONAnd: field L; %w", err)
		}
	}
	return result, nil
}
func (r *And) _unmarshalJSONSlicePredicate(data []byte) ([]Predicate, error) {
	result := make([]Predicate, 0)
	var partial []json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: And._unmarshalJSONSlicePredicate: native list unwrap; %w", err)
	}
	for i, v := range partial {
		item, err := r._unmarshalJSONPredicate(v)
		if err != nil {
			return result, fmt.Errorf("predicate: And._unmarshalJSONSlicePredicate: at index %d; %w", i, err)
		}
		result = append(result, item)
	}
	return result, nil
}
func (r *And) _unmarshalJSONPredicate(data []byte) (Predicate, error) {
	result, err := shared.JSONUnmarshal[Predicate](data)
	if err != nil {
		return result, fmt.Errorf("predicate: And._unmarshalJSONPredicate: native ref unwrap; %w", err)
	}
	return result, nil
}

func OrFromJSON(x []byte) (*Or, error) {
	result := new(Or)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("predicate.OrFromJSON: %w", err)
	}
	return result, nil
}

func OrToJSON(x *Or) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Or)(nil)
	_ json.Marshaler   = (*Or)(nil)
)

func (r *Or) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONOr(*r)
}
func (r *Or) _marshalJSONOr(x Or) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldL []byte
	fieldL, err = r._marshalJSONSlicePredicate(x.L)
	if err != nil {
		return nil, fmt.Errorf("predicate: Or._marshalJSONOr: field name L; %w", err)
	}
	partial["L"] = fieldL
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: Or._marshalJSONOr: struct; %w", err)
	}
	return result, nil
}
func (r *Or) _marshalJSONSlicePredicate(x []Predicate) ([]byte, error) {
	partial := make([]json.RawMessage, len(x))
	for i, v := range x {
		item, err := r._marshalJSONPredicate(v)
		if err != nil {
			return nil, fmt.Errorf("predicate: Or._marshalJSONSlicePredicate: at index %d; %w", i, err)
		}
		partial[i] = item
	}
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: Or._marshalJSONSlicePredicate:; %w", err)
	}
	return result, nil
}
func (r *Or) _marshalJSONPredicate(x Predicate) ([]byte, error) {
	result, err := shared.JSONMarshal[Predicate](x)
	if err != nil {
		return nil, fmt.Errorf("predicate: Or._marshalJSONPredicate:; %w", err)
	}
	return result, nil
}
func (r *Or) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONOr(data)
	if err != nil {
		return fmt.Errorf("predicate: Or.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Or) _unmarshalJSONOr(data []byte) (Or, error) {
	result := Or{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: Or._unmarshalJSONOr: native struct unwrap; %w", err)
	}
	if fieldL, ok := partial["L"]; ok {
		result.L, err = r._unmarshalJSONSlicePredicate(fieldL)
		if err != nil {
			return result, fmt.Errorf("predicate: Or._unmarshalJSONOr: field L; %w", err)
		}
	}
	return result, nil
}
func (r *Or) _unmarshalJSONSlicePredicate(data []byte) ([]Predicate, error) {
	result := make([]Predicate, 0)
	var partial []json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: Or._unmarshalJSONSlicePredicate: native list unwrap; %w", err)
	}
	for i, v := range partial {
		item, err := r._unmarshalJSONPredicate(v)
		if err != nil {
			return result, fmt.Errorf("predicate: Or._unmarshalJSONSlicePredicate: at index %d; %w", i, err)
		}
		result = append(result, item)
	}
	return result, nil
}
func (r *Or) _unmarshalJSONPredicate(data []byte) (Predicate, error) {
	result, err := shared.JSONUnmarshal[Predicate](data)
	if err != nil {
		return result, fmt.Errorf("predicate: Or._unmarshalJSONPredicate: native ref unwrap; %w", err)
	}
	return result, nil
}

func NotFromJSON(x []byte) (*Not, error) {
	result := new(Not)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("predicate.NotFromJSON: %w", err)
	}
	return result, nil
}

func NotToJSON(x *Not) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Not)(nil)
	_ json.Marshaler   = (*Not)(nil)
)

func (r *Not) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONNot(*r)
}
func (r *Not) _marshalJSONNot(x Not) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldP []byte
	fieldP, err = r._marshalJSONPredicate(x.P)
	if err != nil {
		return nil, fmt.Errorf("predicate: Not._marshalJSONNot: field name P; %w", err)
	}
	partial["P"] = fieldP
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: Not._marshalJSONNot: struct; %w", err)
	}
	return result, nil
}
func (r *Not) _marshalJSONPredicate(x Predicate) ([]byte, error) {
	result, err := shared.JSONMarshal[Predicate](x)
	if err != nil {
		return nil, fmt.Errorf("predicate: Not._marshalJSONPredicate:; %w", err)
	}
	return result, nil
}
func (r *Not) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONNot(data)
	if err != nil {
		return fmt.Errorf("predicate: Not.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Not) _unmarshalJSONNot(data []byte) (Not, error) {
	result := Not{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: Not._unmarshalJSONNot: native struct unwrap; %w", err)
	}
	if fieldP, ok := partial["P"]; ok {
		result.P, err = r._unmarshalJSONPredicate(fieldP)
		if err != nil {
			return result, fmt.Errorf("predicate: Not._unmarshalJSONNot: field P; %w", err)
		}
	}
	return result, nil
}
func (r *Not) _unmarshalJSONPredicate(data []byte) (Predicate, error) {
	result, err := shared.JSONUnmarshal[Predicate](data)
	if err != nil {
		return result, fmt.Errorf("predicate: Not._unmarshalJSONPredicate: native ref unwrap; %w", err)
	}
	return result, nil
}

func CompareFromJSON(x []byte) (*Compare, error) {
	result := new(Compare)
	err := result.UnmarshalJSON(x)
	if err != nil {
		return nil, fmt.Errorf("predicate.CompareFromJSON: %w", err)
	}
	return result, nil
}

func CompareToJSON(x *Compare) ([]byte, error) {
	return x.MarshalJSON()
}

var (
	_ json.Unmarshaler = (*Compare)(nil)
	_ json.Marshaler   = (*Compare)(nil)
)

func (r *Compare) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONCompare(*r)
}
func (r *Compare) _marshalJSONCompare(x Compare) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldLocation []byte
	fieldLocation, err = r._marshalJSONstring(x.Location)
	if err != nil {
		return nil, fmt.Errorf("predicate: Compare._marshalJSONCompare: field name Location; %w", err)
	}
	partial["Location"] = fieldLocation
	var fieldOperation []byte
	fieldOperation, err = r._marshalJSONstring(x.Operation)
	if err != nil {
		return nil, fmt.Errorf("predicate: Compare._marshalJSONCompare: field name Operation; %w", err)
	}
	partial["Operation"] = fieldOperation
	var fieldBindValue []byte
	fieldBindValue, err = r._marshalJSONBindable(x.BindValue)
	if err != nil {
		return nil, fmt.Errorf("predicate: Compare._marshalJSONCompare: field name BindValue; %w", err)
	}
	partial["BindValue"] = fieldBindValue
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("predicate: Compare._marshalJSONCompare: struct; %w", err)
	}
	return result, nil
}
func (r *Compare) _marshalJSONstring(x string) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("predicate: Compare._marshalJSONstring:; %w", err)
	}
	return result, nil
}
func (r *Compare) _marshalJSONBindable(x Bindable) ([]byte, error) {
	result, err := shared.JSONMarshal[Bindable](x)
	if err != nil {
		return nil, fmt.Errorf("predicate: Compare._marshalJSONBindable:; %w", err)
	}
	return result, nil
}
func (r *Compare) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONCompare(data)
	if err != nil {
		return fmt.Errorf("predicate: Compare.UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *Compare) _unmarshalJSONCompare(data []byte) (Compare, error) {
	result := Compare{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("predicate: Compare._unmarshalJSONCompare: native struct unwrap; %w", err)
	}
	if fieldLocation, ok := partial["Location"]; ok {
		result.Location, err = r._unmarshalJSONstring(fieldLocation)
		if err != nil {
			return result, fmt.Errorf("predicate: Compare._unmarshalJSONCompare: field Location; %w", err)
		}
	}
	if fieldOperation, ok := partial["Operation"]; ok {
		result.Operation, err = r._unmarshalJSONstring(fieldOperation)
		if err != nil {
			return result, fmt.Errorf("predicate: Compare._unmarshalJSONCompare: field Operation; %w", err)
		}
	}
	if fieldBindValue, ok := partial["BindValue"]; ok {
		result.BindValue, err = r._unmarshalJSONBindable(fieldBindValue)
		if err != nil {
			return result, fmt.Errorf("predicate: Compare._unmarshalJSONCompare: field BindValue; %w", err)
		}
	}
	return result, nil
}
func (r *Compare) _unmarshalJSONstring(data []byte) (string, error) {
	var result string
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("predicate: Compare._unmarshalJSONstring: native primitive unwrap; %w", err)
	}
	return result, nil
}
func (r *Compare) _unmarshalJSONBindable(data []byte) (Bindable, error) {
	result, err := shared.JSONUnmarshal[Bindable](data)
	if err != nil {
		return result, fmt.Errorf("predicate: Compare._unmarshalJSONBindable: native ref unwrap; %w", err)
	}
	return result, nil
}
