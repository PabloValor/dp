<?php

$subNav = array();

set_include_path("../");
include("inc/essentials.php");
?>
<script>
$mainNav.set("home")
</script>

<h1 class="margin-t-0">Typography</h1>
<hr class="light"/>
<p>This is an example page on how to use HTML markup elements and CSS styles included in the Metro UI Template. It is recommend to view the source of this file.
<hr class="dotted margin-t-20"/>
<h2>HTML markup</h2>

<h3>Basic tags</h3>
<p>Use the <code>&lt;p></code> tag to create a new paragraph with some space before and after it.<br />
Use the <code>&lt;br/></code> tag to go to the next line. (aka linebreak).

<p>Use the <code>&lt;em></code> tag to <em>put your text in italic</em><br />
Use the <code>&lt;strong></code> tag to <strong>make it bold</strong><br />
Use the <code>&lt;u></code> tag to <u>underline it</u><br />
Use the <code>&lt;mark></code> tag to <mark>mark your text</mark><br />
Use the <code>&lt;del></code> tag to <del>line-trough your text</del><br />
Use the <code>&lt;small></code> tag for <small>some sidenotes</small><br />
Use the <abbr title="Abbreviation Element">&lt;abbr&gt; tag</abbr> to define an abbreviation and use the <dfn title="Defines a definition term">&lt;dfn&gt; element</dfn> to define a definition term.

<h3>Quotes</h3>
You can use the <q>&lt;q> tag</q> for short <q>quotes</q> or you can use the &lt;blockquote> tag for longer quotes.
<blockquote>A longer quote to demonstrate the styling of the Metro UI Template</blockquote>

<h3>List</h3>
<ul>
	<li>Item 1</li>
	<li>Item 2</li>
</ul>

<h3>Code</h3>
Use the &lt;code> tag to display something as <code>code</code>. To display blocks of code, use the pre and the code tag;
<pre><code>hr.dotted {
	border-top:1px #666 dashed; 
}
hr.light{
	border-color:#999;
}
</code></pre>
<hr class="dotted margin-t-40" />
<h2>CSS styles</h2>
<h3>Tables</h3>
Zebra tables, check source
<table cellspacing="0" width="600" class="table align-center">
<thead>
<tr>
<th width="200" align="left">Heading</th>
<th width="200">Heading</th>
<th width="200" align="right">Heading</th>
</tr>
</thead>

<tbody>
<tr class="dark bold">
<td>Info</td>
<td align="center">Info</td>
<td align="right">Info</td>
</tr>
<tr class="italic">
<td>Info</td>
<td align="center">Info</td>
<td align="right">Info</td>
</tr>
<tr class="dark">
<td>Info</td>
<td align="center">Info</td>
<td align="right">Info</td>
</tr>
</tbody>
<tfoot>
<tr>
<td>Footer</td>
<td align="center">Footer</td>
<td align="right">Footer</td>
</tr>
</tfoot>
</table>

<h3>Boxes</h3>
<div class="box-content">box-content</div>
<div class="box-hint">box-hint</div>
<div class="box-info">box-info</div>
<div class="box-download">box-download</div>
<div class="box-warning">box-warning</div>

<h3>Forms</h3>
<form>
<fieldset>
<legend>Legend</legend>
<label for="f1">Text input:</label> <input id="f1" type="text" value="text input" /><br />
<label for="f2">Radio input:</label> <input id="f2" type="radio" /><br />
<label for="f3">Checkbox input:</label> <input id="f3" type="checkbox" /><br />
<label for="f4">Select:</label>
<select id="f4">
	<option>One</option>
	<option>Two</option>
</select><br /><br />
<label for="f5">Textarea:</label><br />
<textarea id="f5" rows="5" cols="30">Textarea</textarea>
</fieldset>
<button>Button</button> <input type="button" value="Input Button" /><br />
<button class="blueButton">Button</button><button class="greyButton">Button</button><button class="greenButton">Button</button><button class="orangeButton">Button</button><button class="redButton">Button</button>
</form>

<h3>Definition list</h3>
<dl class="separator">
<dt>DEFENITION TERM</dt>
<dd>A defenition description</dd>
<dt>DEFENITION TERM</dt>
<dd>A definition description.</dd>
<dt>DEFENITION TERM</dt>
<dd>A definition description.</dd>
<dd>Another definition description.</dd>
</dl>
<hr class="dotted" />
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>