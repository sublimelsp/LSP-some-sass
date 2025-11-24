# LSP-some-sass

Sass support for Sublime’s LSP.

Provided through [Some Sass language server](https://github.com/wkillerud/some-sass/tree/main/packages/language-server).

### Installation

* Install [LSP](https://packagecontrol.io/packages/LSP) and `LSP-some-sass` via Package Control.
* Install [Sass syntax higlight package](https://packagecontrol.io/packages/Sass).
* Restart Sublime.

### Configuration

There are some ways to configure the package and the language server.

- From `Preferences > Package Settings > LSP > Servers > LSP-some-sass`
- From the command palette `Preferences: LSP-some-sass Settings`

### FAQ

### Using with Vue SFC

When working with Vue SFC, LSP-vue is usually used to provide LSP capabilities to every part of component.

Since LSP-some-sass can be used to process `style[lang="scss"]` blocks in SFCs, CSS language features from LSP-vue
will clash with LSP-some-sass since both are trying to provide information at the same time.

To resolve this, it’s best to disable certain LSP-vue CSS language features and let LSP-some-sass handle that.

`LSP-some-sass.sublime-settings`

* Set `selector` to handle Vue SFC
* Disable default CSS completions and use only Some Sass completions; default CSS completions will come from LSP-vue

```json
{
	"settings": {
		"somesass.scss.completion.css": false
	},
	"selector": "source.scss | text.html.vue"
}
```

`LSP-vue.sublime-settings`

* Disable Sass features:

```json
{
	"settings": {
		"scss.hover.documentation": false,
		"scss.hover.references": false
	}
}
```

Beware that there are certain features that can’t be disabled currently (duplicate color provider references).
