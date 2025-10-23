package questions

import (
	"encoding/json"
	"fmt"
)

// UnmarshalQuestion unmarshals JSON into the appropriate Question type.
func UnmarshalQuestion(data []byte) (Question, error) {
	// First, peek at the question_type
	var wrapper struct {
		QuestionType string `json:"question_type"`
	}
	if err := json.Unmarshal(data, &wrapper); err != nil {
		return nil, fmt.Errorf("failed to unmarshal question_type: %w", err)
	}

	// Based on question_type, unmarshal into the appropriate concrete type
	switch wrapper.QuestionType {
	case "MultipleChoiceEngToLatQuestion":
		var q MultipleChoiceEngToLatQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal MultipleChoiceEngToLatQuestion: %w", err)
		}
		return &q, nil

	case "MultipleChoiceLatToEngQuestion":
		var q MultipleChoiceLatToEngQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal MultipleChoiceLatToEngQuestion: %w", err)
		}
		return &q, nil

	case "ParseWordCompToLatQuestion":
		var q ParseWordCompToLatQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal ParseWordCompToLatQuestion: %w", err)
		}
		return &q, nil

	case "ParseWordLatToCompQuestion":
		var q ParseWordLatToCompQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal ParseWordLatToCompQuestion: %w", err)
		}
		return &q, nil

	case "TypeInEngToLatQuestion":
		var q TypeInEngToLatQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal TypeInEngToLatQuestion: %w", err)
		}
		return &q, nil

	case "TypeInLatToEngQuestion":
		var q TypeInLatToEngQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal TypeInLatToEngQuestion: %w", err)
		}
		return &q, nil

	case "PrincipalPartsQuestion":
		var q PrincipalPartsQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal PrincipalPartsQuestion: %w", err)
		}
		return &q, nil

	default:
		return nil, fmt.Errorf("unknown question_type: %s", wrapper.QuestionType)
	}
}
