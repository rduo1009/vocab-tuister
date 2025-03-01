Set Shell bash
Set Width 2400
Set Height 1200

Require vocab-tuister 

# No arguments given error
Type "GOCOVERDIR=gocov vocab-tuister create-list"
Enter
Wait
Sleep 1

Screenshot tests/integration/client_integration/testdata/no-arguments-create-list.png
Sleep 1

Type "clear"
Enter
Wait
Sleep 1

# No arguments given error
Type "GOCOVERDIR=gocov vocab-tuister create-config"
Enter
Wait
Sleep 1

Screenshot tests/integration/client_integration/testdata/no-arguments-create-config.png
Sleep 1

Type "clear"
Enter
Wait
Sleep 1

# Invalid number of questions
Type "GOCOVERDIR=gocov vocab-tuister session --number -1 --session-config tests/examples/example-config.json --vocab-list tests/examples/example-list.txt"
Enter
Wait
Sleep 1

Screenshot tests/integration/client_integration/testdata/invalid-questionsnum-session.png
Sleep 1

Type "clear"
Enter
Wait
Sleep 1

# Invalid port
Type "GOCOVERDIR=gocov vocab-tuister session --number 1 --session-config tests/examples/example-config.json --vocab-list tests/examples/example-list.txt --server-port -1"
Enter
Wait
Sleep 1

Screenshot tests/integration/client_integration/testdata/invalid-port-session.png
Sleep 1

Type "clear"
Enter
Wait
Sleep 1
