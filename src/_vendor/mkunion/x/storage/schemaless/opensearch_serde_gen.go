// Code generated by mkunion. DO NOT EDIT.
package schemaless

import (
	"encoding/json"
	"fmt"
	"github.com/widmogrod/mkunion/x/shared"
)

var (
	_ json.Unmarshaler = (*OpenSearchSearchResult[any])(nil)
	_ json.Marshaler   = (*OpenSearchSearchResult[any])(nil)
)

func (r *OpenSearchSearchResult[A]) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONOpenSearchSearchResultLb_A_bL(*r)
}
func (r *OpenSearchSearchResult[A]) _marshalJSONOpenSearchSearchResultLb_A_bL(x OpenSearchSearchResult[A]) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldHits []byte
	fieldHits, err = r._marshalJSONOpenSearchSearchResultHitsLb_A_bL(x.Hits)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResult[A]._marshalJSONOpenSearchSearchResultLb_A_bL: field name Hits; %w", err)
	}
	partial["hits"] = fieldHits
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResult[A]._marshalJSONOpenSearchSearchResultLb_A_bL: struct; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResult[A]) _marshalJSONOpenSearchSearchResultHitsLb_A_bL(x OpenSearchSearchResultHits[A]) ([]byte, error) {
	result, err := shared.JSONMarshal[OpenSearchSearchResultHits[A]](x)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResult[A]._marshalJSONOpenSearchSearchResultHitsLb_A_bL:; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResult[A]) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONOpenSearchSearchResultLb_A_bL(data)
	if err != nil {
		return fmt.Errorf("schemaless: OpenSearchSearchResult[A].UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *OpenSearchSearchResult[A]) _unmarshalJSONOpenSearchSearchResultLb_A_bL(data []byte) (OpenSearchSearchResult[A], error) {
	result := OpenSearchSearchResult[A]{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResult[A]._unmarshalJSONOpenSearchSearchResultLb_A_bL: native struct unwrap; %w", err)
	}
	if fieldHits, ok := partial["hits"]; ok {
		result.Hits, err = r._unmarshalJSONOpenSearchSearchResultHitsLb_A_bL(fieldHits)
		if err != nil {
			return result, fmt.Errorf("schemaless: OpenSearchSearchResult[A]._unmarshalJSONOpenSearchSearchResultLb_A_bL: field Hits; %w", err)
		}
	}
	return result, nil
}
func (r *OpenSearchSearchResult[A]) _unmarshalJSONOpenSearchSearchResultHitsLb_A_bL(data []byte) (OpenSearchSearchResultHits[A], error) {
	result, err := shared.JSONUnmarshal[OpenSearchSearchResultHits[A]](data)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResult[A]._unmarshalJSONOpenSearchSearchResultHitsLb_A_bL: native ref unwrap; %w", err)
	}
	return result, nil
}

var (
	_ json.Unmarshaler = (*OpenSearchSearchResultHit[any])(nil)
	_ json.Marshaler   = (*OpenSearchSearchResultHit[any])(nil)
)

func (r *OpenSearchSearchResultHit[A]) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONOpenSearchSearchResultHitLb_A_bL(*r)
}
func (r *OpenSearchSearchResultHit[A]) _marshalJSONOpenSearchSearchResultHitLb_A_bL(x OpenSearchSearchResultHit[A]) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldItem []byte
	fieldItem, err = r._marshalJSONA(x.Item)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._marshalJSONOpenSearchSearchResultHitLb_A_bL: field name Item; %w", err)
	}
	partial["_source"] = fieldItem
	var fieldSort []byte
	fieldSort, err = r._marshalJSONSlicestring(x.Sort)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._marshalJSONOpenSearchSearchResultHitLb_A_bL: field name Sort; %w", err)
	}
	partial["sort"] = fieldSort
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._marshalJSONOpenSearchSearchResultHitLb_A_bL: struct; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHit[A]) _marshalJSONA(x A) ([]byte, error) {
	result, err := shared.JSONMarshal[A](x)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._marshalJSONA:; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHit[A]) _marshalJSONSlicestring(x []string) ([]byte, error) {
	partial := make([]json.RawMessage, len(x))
	for i, v := range x {
		item, err := r._marshalJSONstring(v)
		if err != nil {
			return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._marshalJSONSlicestring: at index %d; %w", i, err)
		}
		partial[i] = item
	}
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._marshalJSONSlicestring:; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHit[A]) _marshalJSONstring(x string) ([]byte, error) {
	result, err := json.Marshal(x)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._marshalJSONstring:; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHit[A]) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONOpenSearchSearchResultHitLb_A_bL(data)
	if err != nil {
		return fmt.Errorf("schemaless: OpenSearchSearchResultHit[A].UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *OpenSearchSearchResultHit[A]) _unmarshalJSONOpenSearchSearchResultHitLb_A_bL(data []byte) (OpenSearchSearchResultHit[A], error) {
	result := OpenSearchSearchResultHit[A]{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._unmarshalJSONOpenSearchSearchResultHitLb_A_bL: native struct unwrap; %w", err)
	}
	if fieldItem, ok := partial["_source"]; ok {
		result.Item, err = r._unmarshalJSONA(fieldItem)
		if err != nil {
			return result, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._unmarshalJSONOpenSearchSearchResultHitLb_A_bL: field Item; %w", err)
		}
	}
	if fieldSort, ok := partial["sort"]; ok {
		result.Sort, err = r._unmarshalJSONSlicestring(fieldSort)
		if err != nil {
			return result, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._unmarshalJSONOpenSearchSearchResultHitLb_A_bL: field Sort; %w", err)
		}
	}
	return result, nil
}
func (r *OpenSearchSearchResultHit[A]) _unmarshalJSONA(data []byte) (A, error) {
	result, err := shared.JSONUnmarshal[A](data)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._unmarshalJSONA: native ref unwrap; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHit[A]) _unmarshalJSONSlicestring(data []byte) ([]string, error) {
	result := make([]string, 0)
	var partial []json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._unmarshalJSONSlicestring: native list unwrap; %w", err)
	}
	for i, v := range partial {
		item, err := r._unmarshalJSONstring(v)
		if err != nil {
			return result, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._unmarshalJSONSlicestring: at index %d; %w", i, err)
		}
		result = append(result, item)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHit[A]) _unmarshalJSONstring(data []byte) (string, error) {
	var result string
	err := json.Unmarshal(data, &result)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResultHit[A]._unmarshalJSONstring: native primitive unwrap; %w", err)
	}
	return result, nil
}

var (
	_ json.Unmarshaler = (*OpenSearchSearchResultHits[any])(nil)
	_ json.Marshaler   = (*OpenSearchSearchResultHits[any])(nil)
)

func (r *OpenSearchSearchResultHits[A]) MarshalJSON() ([]byte, error) {
	if r == nil {
		return nil, nil
	}
	return r._marshalJSONOpenSearchSearchResultHitsLb_A_bL(*r)
}
func (r *OpenSearchSearchResultHits[A]) _marshalJSONOpenSearchSearchResultHitsLb_A_bL(x OpenSearchSearchResultHits[A]) ([]byte, error) {
	partial := make(map[string]json.RawMessage)
	var err error
	var fieldHits []byte
	fieldHits, err = r._marshalJSONSliceOpenSearchSearchResultHitLb_A_bL(x.Hits)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._marshalJSONOpenSearchSearchResultHitsLb_A_bL: field name Hits; %w", err)
	}
	partial["hits"] = fieldHits
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._marshalJSONOpenSearchSearchResultHitsLb_A_bL: struct; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHits[A]) _marshalJSONSliceOpenSearchSearchResultHitLb_A_bL(x []OpenSearchSearchResultHit[A]) ([]byte, error) {
	partial := make([]json.RawMessage, len(x))
	for i, v := range x {
		item, err := r._marshalJSONOpenSearchSearchResultHitLb_A_bL(v)
		if err != nil {
			return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._marshalJSONSliceOpenSearchSearchResultHitLb_A_bL: at index %d; %w", i, err)
		}
		partial[i] = item
	}
	result, err := json.Marshal(partial)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._marshalJSONSliceOpenSearchSearchResultHitLb_A_bL:; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHits[A]) _marshalJSONOpenSearchSearchResultHitLb_A_bL(x OpenSearchSearchResultHit[A]) ([]byte, error) {
	result, err := shared.JSONMarshal[OpenSearchSearchResultHit[A]](x)
	if err != nil {
		return nil, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._marshalJSONOpenSearchSearchResultHitLb_A_bL:; %w", err)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHits[A]) UnmarshalJSON(data []byte) error {
	result, err := r._unmarshalJSONOpenSearchSearchResultHitsLb_A_bL(data)
	if err != nil {
		return fmt.Errorf("schemaless: OpenSearchSearchResultHits[A].UnmarshalJSON: %w", err)
	}
	*r = result
	return nil
}
func (r *OpenSearchSearchResultHits[A]) _unmarshalJSONOpenSearchSearchResultHitsLb_A_bL(data []byte) (OpenSearchSearchResultHits[A], error) {
	result := OpenSearchSearchResultHits[A]{}
	var partial map[string]json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._unmarshalJSONOpenSearchSearchResultHitsLb_A_bL: native struct unwrap; %w", err)
	}
	if fieldHits, ok := partial["hits"]; ok {
		result.Hits, err = r._unmarshalJSONSliceOpenSearchSearchResultHitLb_A_bL(fieldHits)
		if err != nil {
			return result, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._unmarshalJSONOpenSearchSearchResultHitsLb_A_bL: field Hits; %w", err)
		}
	}
	return result, nil
}
func (r *OpenSearchSearchResultHits[A]) _unmarshalJSONSliceOpenSearchSearchResultHitLb_A_bL(data []byte) ([]OpenSearchSearchResultHit[A], error) {
	result := make([]OpenSearchSearchResultHit[A], 0)
	var partial []json.RawMessage
	err := json.Unmarshal(data, &partial)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._unmarshalJSONSliceOpenSearchSearchResultHitLb_A_bL: native list unwrap; %w", err)
	}
	for i, v := range partial {
		item, err := r._unmarshalJSONOpenSearchSearchResultHitLb_A_bL(v)
		if err != nil {
			return result, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._unmarshalJSONSliceOpenSearchSearchResultHitLb_A_bL: at index %d; %w", i, err)
		}
		result = append(result, item)
	}
	return result, nil
}
func (r *OpenSearchSearchResultHits[A]) _unmarshalJSONOpenSearchSearchResultHitLb_A_bL(data []byte) (OpenSearchSearchResultHit[A], error) {
	result, err := shared.JSONUnmarshal[OpenSearchSearchResultHit[A]](data)
	if err != nil {
		return result, fmt.Errorf("schemaless: OpenSearchSearchResultHits[A]._unmarshalJSONOpenSearchSearchResultHitLb_A_bL: native ref unwrap; %w", err)
	}
	return result, nil
}