Set Shell bash
Set Width 2400
Set Height 1200

Require vocab-tuister 

# No arguments given error
Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister create-list"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/no-arguments-create-list.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1

# No arguments given error
Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister create-config"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/no-arguments-create-config.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1

# Invalid number of questions
Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister session --number -1 --session-config tests/examples/example-config.json --vocab-list tests/examples/example-list.txt"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/invalid-questionsnum-session.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1

# Invalid port
Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister session --number 1 --session-config tests/examples/example-config.json --vocab-list tests/examples/example-list.txt --server-port -1"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/invalid-port-session.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1
