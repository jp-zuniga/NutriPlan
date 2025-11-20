<script>
	import { authUser } from '$lib/stores/auth';
	import { API_CREATE_ARTICLE_ENDPOINT } from '$lib/endpoints';
	import { goto } from '$app/navigation';
	import { marked } from 'marked';
	import { render } from 'svelte/server';
	import { authenticatedFetch, JSONRequest } from '$lib/utils/fetch';
	import RotatingNutriplan from './RotatingNutriplan.svelte';

	let title = $state('');
	let content = $state('');
	let loading = $state(false);
	let error = $state('');
	let success = $state(false);

	// Función para verificar si el usuario puede crear artículos
	function canCreateArticles() {
		return $authUser && ($authUser.role === 'staff' || $authUser.role === 'admin');
	}

	// Función para crear el artículo
	async function createArticle() {
		if (!canCreateArticles()) {
			error = 'No tienes permisos para crear artículos';
			return;
		}

		if (!title.trim() || !content.trim()) {
			error = 'Título y contenido son requeridos';
			return;
		}

		loading = true;
		error = '';

		try {
			const response = await fetch(
				'/api/article',
				JSONRequest({
					title: title.trim(),
					text: content.trim()
				})
			);

			if (response.ok) {
				const data = await response.json();
				success = true;
				// Redirigir al artículo creado después de un breve delay
				setTimeout(() => {
					goto(`/articulos`);
				}, 2000);
			} else {
				const errorData = await response.json();
				error = errorData.error || 'Error al crear el artículo';
			}
		} catch (err) {
			console.error('Error creating article:', err);
			error = 'Error de conexión. Inténtalo de nuevo.';
		}

		loading = false;
	}

	// Función para resetear el formulario
	function resetForm() {
		title = '';
		content = '';
		error = '';
		success = false;
	}

	let renderedContent = $state('');

	$effect(() => {
		try {
			renderedContent = marked(content);
		} catch (err) {
			renderedContent = `<p class="p-emphasis">Invalid Markdown: ${err}</p>`;
		}
	});
</script>

{#if $authUser === undefined}
	<div class="flex-center" style="height: calc(100vh - 75px)">
		<RotatingNutriplan />
	</div>
{:else if !canCreateArticles()}
	<div class="permission-denied flex-center direction-col pad-50">
		<i class="las la-lock" style="font-size: 48px; color: var(--color-soft); margin-bottom: 16px;"
		></i>
		<h2 class="h2 bold mb">Acceso Restringido</h2>
		<p class="lg-p p-ghost txt-center">
			Solo usuarios con rol de staff o admin pueden crear artículos.
		</p>
		<a href="/articulos" class="btn primary mt">Volver a artículos</a>
	</div>
{:else}
	<div class="form-header mb-l">
		<h1 class="h1 bold mb">Crear Nuevo Artículo</h1>
		<p class="lg-p p-ghost">
			Comparte tu conocimiento sobre nutrición y bienestar con la comunidad.
		</p>
	</div>
	<div class="content regrid-cols-2">
		<div class="article-form-container">
			{#if success}
				<div class="success-message bg-soft-gray pad-20 round-10 mb-l">
					<div class="flex items-center gap-16">
						<i
							class="las la-check-circle"
							style="font-size: 24px; color: var(--color-primary-dark);"
						></i>
						<div>
							<h3 class="h3 bold">¡Artículo creado exitosamente!</h3>
							<p class="md-p p-ghost">Redirigiendo al artículo...</p>
						</div>
					</div>
				</div>
			{/if}
			{#if error}
				<div class="error-message bg-soft-gray pad-20 round-10 mb-l">
					<div class="flex items-center gap-16">
						<i
							class="las la-exclamation-triangle"
							style="font-size: 24px; color: var(--color-emphasis);"
						></i>
						<div>
							<h3 class="h3 bold">Error</h3>
							<p class="md-p">{error}</p>
						</div>
					</div>
				</div>
			{/if}
			<form
				onsubmit={(e) => {
					e.preventDefault();
					createArticle();
				}}
				class="article-form"
			>
				<div class="form-group mb-l">
					<label for="title" class="label bold mb-s">Título del Artículo</label>
					<input
						type="text"
						id="title"
						bind:value={title}
						placeholder="Escribe un título atractivo para tu artículo..."
						class="form-input full-width"
						required
						disabled={loading}
					/>
				</div>
				<div class="form-group mb-l">
					<label for="author" class="label bold mb-s">Autor</label>
					<input
						type="text"
						required
						id="author"
						value={$authUser?.first_name + ' ' + $authUser?.last_name ||
							$authUser?.email ||
							'Usuario'}
						class="form-input full-width"
						readonly
						disabled
					/>
					<p class="sm-p p-ghost mt-s">
						Este campo se llena automáticamente con tu información de usuario.
					</p>
				</div>
				<div class="form-group mb-l">
					<label for="content" class="label bold mb-s">Contenido (Markdown)</label>
					<div class="editor-container">
						<textarea
							bind:value={content}
							placeholder="Escribe el contenido de tu artículo en markdown..."
							class="markdown-textarea full-width"
							disabled={loading}
						></textarea>
					</div>
					<p class="sm-p p-ghost mt-s">
						Puedes usar markdown para formatear tu contenido. Usa **texto en negrita**, *texto en
						cursiva*, # para títulos, etc.
					</p>
				</div>
				<div class="form-actions flex gap-16">
					<button type="button" class="btn ghost" onclick={resetForm} disabled={loading}>
						Limpiar
					</button>
					<button
						type="submit"
						class="btn primary"
						disabled={loading || !title.trim() || !content.trim()}
					>
						{#if loading}
							<i class="las la-spinner la-spin"></i>
							Creando...
						{:else}
							<i class="las la-plus"></i>
							Crear Artículo
						{/if}
					</button>
				</div>
			</form>
		</div>
		<div class="render pad-20">
			{@html renderedContent}
		</div>
	</div>
{/if}

<style>
	.permission-denied {
		text-align: center;
		min-height: 400px;
	}

	.article-form-container {
		max-width: 800px;
		margin: 0 auto;
	}

	.form-header {
		text-align: center;
		padding-bottom: 20px;
		border-bottom: 1px solid var(--color-soft-gray);
	}

	.success-message {
		border-left: 4px solid var(--color-primary-dark);
	}

	.error-message {
		border-left: 4px solid var(--color-emphasis);
	}

	.article-form {
		background: white;
		padding: 30px;
		border-radius: 12px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.form-group {
		margin-bottom: 24px;
	}

	.label {
		display: block;
		color: var(--color-forest);
		font-size: 1rem;
	}

	.form-input {
		padding: 12px 16px;
		border: 1px solid var(--color-soft-gray);
		border-radius: 8px;
		font-size: 1rem;
		transition:
			border-color 0.2s ease,
			box-shadow 0.2s ease;
	}

	.form-input:focus {
		outline: none;
		border-color: var(--color-primary-dark);
		box-shadow: 0 0 0 3px rgba(108, 144, 115, 0.1);
	}

	.form-input:disabled {
		background-color: var(--color-soft-gray);
		color: var(--color-soft);
		cursor: not-allowed;
	}

	.editor-container {
		border: 1px solid var(--color-soft-gray);
		border-radius: 8px;
		overflow: hidden;
	}

	.markdown-textarea {
		min-height: 400px;
		padding: 16px;
		border: none;
		border-radius: 8px;
		font-family: 'Courier New', monospace;
		font-size: 14px;
		line-height: 1.6;
		resize: vertical;
		background: white;
	}

	.markdown-textarea:focus {
		outline: none;
		background: var(--color-soft-white);
	}

	.form-actions {
		padding-top: 20px;
		border-top: 1px solid var(--color-soft-gray);
		justify-content: flex-end;
	}

	.btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.btn i {
		margin-right: 8px;
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}

	.la-spin {
		animation: spin 1s linear infinite;
	}
</style>
