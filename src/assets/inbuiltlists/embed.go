// Package inbuiltlists contains vocab lists from various Latin textbooks.
//
// Included textbook vocab lists:
//   - Cambridge Latin Course (4th edition)
//   - Latin to GCSE (parts 1 and 2)
package inbuiltlists

import "embed"

//go:embed *
var InbuiltLists embed.FS
