<script>
	export let collection;
	export let showActions = false;
	export let onEdit = null;
	export let onDelete = null;

	const getPreviewImages = (items) => {
		if (!items || items.length === 0) return [];
		return items
			.slice(0, 4)
			.map((item) => item.recipe?.images?.[0]?.image?.url || '/placeholder-recipe.jpg');
	};

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('es-ES', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	};

	const handleEdit = () => {
		if (onEdit) {
			onEdit(collection);
		} else {
			console.log('Edit collection', collection.id);
		}
	};

	const handleDelete = () => {
		if (onDelete) {
			onDelete(collection.id);
		} else {
			console.log('Delete collection', collection.id);
		}
	};
</script>

<article class="card hoverable b-shadow">
	<div class="collection-preview">
		{#if collection.items && collection.items.length > 0}
			<div class="preview-grid">
				{#each getPreviewImages(collection.items) as image, index}
					<div class="preview-image" style="background-image: url({image})">
						{#if index === 3 && collection.items.length > 4}
							<div class="more-count">+{collection.items.length - 4}</div>
						{/if}
					</div>
				{/each}
			</div>
		{:else}
			<div class="empty-preview">
				<i class="las la-folder-open"></i>
				<p class="sm-p p-ghost">Sin recetas</p>
			</div>
		{/if}
	</div>

	<div class="collection-info pad-20">
		<div class="collection-header">
			<h3 class="h3 bold text-col-1">{collection.name}</h3>
			{#if collection.is_public}
				<span class="tag">Pública</span>
			{/if}
		</div>

		{#if collection.description}
			<p class="md-p text-col-2 mb-s">{collection.description}</p>
		{/if}

		<div class="collection-meta flex justify-between items-center">
			<div class="stats">
				<span class="sm-p text-col-2">
					<i class="las la-utensils"></i>
					{collection.items?.length || 0} recetas
				</span>
				<span class="sm-p text-col-2">
					<i class="las la-calendar"></i>
					{formatDate(collection.created_at)}
				</span>
			</div>

			{#if showActions}
				<div class="actions">
					<button class="btn ghost" onclick={handleEdit} aria-label="Editar colección">
						<i class="las la-edit"></i>
					</button>
					<button class="btn ghost" onclick={handleDelete} aria-label="Eliminar colección">
						<i class="las la-trash"></i>
					</button>
				</div>
			{/if}
		</div>
	</div>
</article>

<style>
	.collection-preview {
		height: 120px;
		overflow: hidden;
		border-radius: var(--radius-md) var(--radius-md) 0 0;
	}

	.preview-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		grid-template-rows: 1fr 1fr;
		height: 100%;
		gap: 2px;
	}

	.preview-image {
		background-size: cover;
		background-position: center;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.more-count {
		background: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 0.25rem 0.5rem;
		border-radius: 999px;
		font-size: 0.75rem;
		font-weight: 600;
	}

	.empty-preview {
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: var(--color-soft-gray);
		color: var(--color-soft);
	}

	.empty-preview i {
		font-size: 2rem;
		margin-bottom: 0.5rem;
	}

	.collection-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.collection-header h3 {
		margin: 0;
		flex: 1;
		line-height: 1.3;
	}

	.collection-meta {
		margin-top: 1rem;
	}

	.stats {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.stats span {
		display: flex;
		align-items: center;
		gap: 0.25rem;
	}

	.actions {
		display: flex;
		gap: 0.5rem;
	}

	.actions .btn {
		padding: 0.5rem;
		min-width: auto;
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	@media (max-width: 640px) {
		.collection-header {
			flex-direction: column;
			align-items: flex-start;
		}

		.collection-meta {
			flex-direction: column;
			align-items: flex-start;
			gap: 1rem;
		}
	}
</style>
