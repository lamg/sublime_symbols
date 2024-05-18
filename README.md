# Sublime Symbols

Sublime Text extension for typing Unicode characters. It works by detecting a sequence of characters and replacing it by some preconfigured string, which usually is an Unicode character, but can be something else.

Recognized sequences are independent of the plugin itself, thus can be customized easily since they are just
JSON objects like the following:

```json
{
	":eq:": "≡",
	":and:": "∧"
}
```