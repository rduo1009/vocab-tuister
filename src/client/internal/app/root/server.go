package root

const (
	vocabListPage     = "send-vocab"
	sessionConfigPage = "send-config"
)

type ErrorResponse struct {
	ErrorType string `json:"error"`
	Message   string `json:"message"`
	Details   string `json:"details,omitempty"`
}
