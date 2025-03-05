Set Shell bash
Set Width 2400
Set Height 1200

Require vocab-tuister

Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister --help"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/help-root.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister create-list --help"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/help-create-list.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister create-config --help"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/help-create-config.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Type "GOCOVERDIR=reports/coverage/go-integration vocab-tuister session --help"
Enter
Wait+Screen /bash-5.2/
Sleep 1

Screenshot tests/integration/client_integration/testdata/help-session.png
Sleep 1

Type "clear"
Enter
Wait+Screen /bash-5.2/
Sleep 1
