package main

//go:generate go run structs_generator.go
//go:generate python3 scripts/create_settings_json.py
//go:generate gojsonstruct --typename SessionConfig --package-name pkg --file-header "// Code generated by gojsonstruct; DO NOT EDIT." -o client/pkg/sessionconfig.go scripts/json_output/Settings_sample.json

//go:generate mkunion watch -g client/pkg/questions/questions.go
//go:generate mkunion
//go:generate patch client/pkg/questions/types_reg_gen.go client/pkg/questions/types_reg_gen_fix.diff

//go:generate enumer -type=Number,Tense,Voice,Mood,Case,Gender,Degree -transform=snake -output client/pkg/enums/ending_components_enumer_gen.go client/pkg/enums/ending_components.go