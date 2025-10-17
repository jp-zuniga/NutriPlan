<script>
	import Checkbox from '$lib/components/Checkbox.svelte';
</script>

<div class="pad-20 bg-white">
	<p class="h1">header 1</p>
	<p class="h2">header 2</p>
	<p class="h3">header 3</p>
	<p class="lg-p">Large Paragraph</p>
	<p class="md-p">Medium Paragraph</p>
	<p class="sm-p">Small Paragraph</p>
	<p class="p-emphasis">Emphasis</p>
	<p class="p-ghost">Ghost</p>
	<button class="btn primary">Primary Button</button>
	<button class="btn ghost">Secondary Button</button>
	<p class="md-p">Input</p>
	<input type="text" />
	<p class="md-p">Select</p>
	<select name="" id="">
		<option value="">Choose option</option>
	</select>
	<Checkbox checked="true" label="Checked" />
	<Checkbox checked="false" label="Unchecked" />
</div>

<div class="pad-20 bg-white" style="background-color: rgb(50,50,50)">
	<p class="h1" style="color: white">header 1</p>
	<p class="h2" style="color: white">header 2</p>
	<p class="h3" style="color: white">header 3</p>
	<p class="lg-p" style="color: white">Large Paragraph</p>
	<p class="md-p" style="color: white">Medium Paragraph</p>
	<p class="sm-p" style="color: white">Small Paragraph</p>

	<p class="p-emphasis" style="color:orange; text-decoration-color:orange;">Emphasis</p>
	<p class="p-ghost" style="color: white">Ghost</p>
	<button class="btn primary">Primary Button</button>
	<button class="btn ghost">Secondary Button</button>
	<p class="md-p" style="color:white">Input</p>
	<input type="text" />
	<p class="md-p" style="color:white">Select</p>
	<select name="" id="">
		<option value="">Choose option</option>
	</select>
	<Checkbox checked="true" label="Checked" />
	<Checkbox checked="false" label="Unchecked" />
</div>
