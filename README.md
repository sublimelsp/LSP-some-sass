# LSP-sass

Sass support for Sublime’s LSP.

Provided through [Some Sass language server](https://github.com/wkillerud/some-sass/tree/main/packages/language-server).

### Installation

* Install [LSP](https://packagecontrol.io/packages/LSP) and `LSP-sass` via Package Control.
* Install [Sass syntax higlight package](https://packagecontrol.io/packages/Sass).
* Restart Sublime.

### Configuration

There are some ways to configure the package and the language server.

- From `Preferences > Package Settings > LSP > Servers > LSP-sass`
- From the command palette `Preferences: LSP-sass Settings`

### FAQ

### Using with Vue SFC

When working with Vue SFC, LSP-volar is usually used to provide LSP capabilities to every part of component.

Since LSP-sass can be used to process `style[lang="scss"]` blocks in SFCs, CSS language features from LSP-volar
will clash with LSP-sass since both are trying to provide information at the same time.

To resolve this, it’s best to disable certain LSP-volar CSS language features and let LSP-sass handle that.

* In `LSP-sass.sublime-settings` set `selector` to handle Vue SFC:

```json
{
	"selector": "source.scss | text.html.vue"
}
```

* In `LSP-volar.sublime-settings` disable Sass features:

```json
{
	"settings": {
		"scss.hover.documentation": false,
		"scss.hover.references": false
	}
}
```

Beware that there are certain features that can’t be disabled currently (duplicate color provider references).
