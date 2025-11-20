<script>
	import Banner from '$lib/components/Banner.svelte';
	import CollectionCard from '$lib/components/CollectionCard.svelte';
	import { authUser } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';
	import { API_COLLECTIONS_ENDPOINT, API_ME_ENDPOINT } from '$lib/endpoints';
	import { authenticatedFetch } from '$lib/utils/fetch';

	$effect(() => {
		if ($authUser === null) goto('/login');
	});

	// Estados para colecciones
	let collections = $state([]);
	let loadingCollections = $state(true);
	let errorCollections = $state(null);
	let showCreateForm = $state(false);

	// Estados para datos del usuario
	let userProfile = $state(null);
	let loadingProfile = $state(true);
	let errorProfile = $state(null);
	let showEditProfile = $state(false);
	let editingProfile = $state({});

	// Formulario para crear colección
	let newCollection = $state({
		name: '',
		description: '',
		is_public: false
	});

	// Funciones para manejar colecciones
	const fetchCollections = async () => {
		try {
			loadingCollections = true;
			errorCollections = null;

			const response = await authenticatedFetch(API_COLLECTIONS_ENDPOINT, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				const data = await response.json();
				collections = data.results || data;
				console.log('Collections loaded:', collections);
			} else if (response.status === 401) {
				errorCollections = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
			} else {
				const errorData = await response.json().catch(() => ({}));
				errorCollections = errorData.detail || `Error ${response.status}: ${response.statusText}`;
			}
		} catch (err) {
			errorCollections = 'Error de conexión con el servidor';
			console.error('Error fetching collections:', err);
		} finally {
			loadingCollections = false;
		}
	};

	const fetchUserProfile = async () => {
		try {
			loadingProfile = true;
			errorProfile = null;

			const response = await fetch(API_ME_ENDPOINT, {
				method: 'GET',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				userProfile = await response.json();
				console.log('User profile loaded:', userProfile);
			} else if (response.status === 401) {
				errorProfile = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
			} else {
				const errorData = await response.json().catch(() => ({}));
				errorProfile = errorData.detail || `Error ${response.status}: ${response.statusText}`;
			}
		} catch (err) {
			errorProfile = 'Error de conexión con el servidor';
			console.error('Error fetching profile:', err);
		} finally {
			loadingProfile = false;
		}
	};

	const createCollection = async (event) => {
		event.preventDefault();
		try {
			const response = await fetch(API_COLLECTIONS_ENDPOINT, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				credentials: 'include',
				body: JSON.stringify(newCollection)
			});

			if (response.ok) {
				const createdCollection = await response.json();
				console.log('Collection created:', createdCollection);
				// Resetear formulario
				newCollection = { name: '', description: '', is_public: false };
				showCreateForm = false;
				// Recargar colecciones
				await fetchCollections();
			} else if (response.status === 401) {
				errorCollections = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
				goto('/login');
			} else {
				const errorData = await response.json().catch(() => ({}));
				errorCollections = errorData.detail || `Error ${response.status}: ${response.statusText}`;
			}
		} catch (err) {
			errorCollections = 'Error de conexión con el servidor';
			console.error('Error creating collection:', err);
		}
	};

	// Función para eliminar colección
	const deleteCollection = async (collectionId) => {
		if (!confirm('¿Estás seguro de que quieres eliminar esta colección?')) {
			return;
		}

		try {
			const response = await fetch(`${API_COLLECTIONS_ENDPOINT}${collectionId}/`, {
				method: 'DELETE',
				credentials: 'include'
			});

			if (response.ok) {
				await fetchCollections(); // Recargar lista
			} else if (response.status === 401) {
				errorCollections = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
				goto('/login');
			} else {
				const errorData = await response.json().catch(() => ({}));
				errorCollections = errorData.detail || `Error ${response.status}: ${response.statusText}`;
			}
		} catch (err) {
			errorCollections = 'Error de conexión con el servidor';
			console.error('Error deleting collection:', err);
		}
	};

	// Función para actualizar perfil
	const updateProfile = async (profileData) => {
		try {
			const response = await fetch(API_ME_ENDPOINT, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json'
				},
				credentials: 'include',
				body: JSON.stringify(profileData)
			});

			if (response.ok) {
				userProfile = await response.json();
				console.log('Profile updated:', userProfile);
			} else if (response.status === 401) {
				errorProfile = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
				goto('/login');
			} else {
				const errorData = await response.json().catch(() => ({}));
				errorProfile = errorData.detail || `Error ${response.status}: ${response.statusText}`;
			}
		} catch (err) {
			errorProfile = 'Error de conexión con el servidor';
			console.error('Error updating profile:', err);
		}
	};

	// Función para iniciar edición de perfil
	const startEditProfile = () => {
		editingProfile = {
			first_name: userProfile?.first_name || '',
			last_name: userProfile?.last_name || '',
			phone_number: userProfile?.phone_number || ''
		};
		showEditProfile = true;
	};

	// Función para guardar cambios del perfil
	const saveProfile = async () => {
		await updateProfile(editingProfile);
		showEditProfile = false;
	};

	// Función para cancelar edición
	const cancelEditProfile = () => {
		showEditProfile = false;
		editingProfile = {};
	};

	onMount(() => {
		if ($authUser) {
			fetchCollections();
			fetchUserProfile();
		}
	});
</script>

{#if $authUser !== undefined && $authUser !== null}
	<main class="profile">
		<!-- Hero Section -->
		<section class="section hero-gradient">
			<div class="container">
				<div class="grid regrid-cols-2 gap-32">
					<article class="card hero-card pad-20">
						<div class="flex direction-col gap-16">
							<div class="user-header flex items-center">
								<div class="avatar">
									<i class="las la-user"></i>
								</div>
								<div class="flex direction-col">
									<p class="h2 bold no-margin">
										{userProfile?.first_name || $authUser?.first_name || 'Usuario'}
										{userProfile?.last_name || $authUser?.last_name || ''}
									</p>
									<p class="md-p p-ghost no-margin">Miembro desde 2025</p>
								</div>
							</div>
						</div>
					</article>

					<section class="card pad-20 bg-gradient-mint">
						<h2 class="h2 bold text-col-white no-margin no-pad mb">Restricciones dietéticas</h2>
						{#if loadingProfile}
							<div class="flex-center">
								<RotatingNutriplan />
							</div>
						{:else if userProfile?.dietary_restrictions?.length > 0}
							<div class="flex wrap gap-8">
								{#each userProfile.dietary_restrictions as restriction}
									<span class="chip bg-white text-col-1">{restriction.name}</span>
								{/each}
							</div>
						{:else}
							<p class="text-col-white p-ghost">No tienes restricciones dietéticas registradas</p>
							<button class="btn ghost text-col-white mt">
								<i class="las la-plus"></i> Agregar restricciones
							</button>
						{/if}
					</section>
				</div>
			</div>
		</section>

		<!-- Colecciones Section -->
		<section class="section bg-soft">
			<div class="container">
				<div class="flex justify-between items-center mb-24">
					<div>
						<h2 class="h2 bold text-col-1">Mis Colecciones</h2>
						<p class="md-p text-col-2">
							Organiza tus recetas favoritas en colecciones personalizadas
						</p>
					</div>
					<button class="btn primary" onclick={() => (showCreateForm = !showCreateForm)}>
						<i class="las la-plus"></i> Nueva Colección
					</button>
				</div>

				<!-- Formulario para crear colección -->
				{#if showCreateForm}
					<div class="card pad-20 mb-24 bg-gradient-sunrise">
						<h3 class="h3 bold text-col-white mb">Crear Nueva Colección</h3>
						<form onsubmit={createCollection} class="flex direction-col gap-16">
							<div class="flex direction-col gap-8">
								<label for="collection-name" class="text-col-white">Nombre de la colección</label>
								<input
									id="collection-name"
									type="text"
									bind:value={newCollection.name}
									placeholder="Ej: Recetas de desayuno"
									required
									class="bg-white"
								/>
							</div>
							<div class="flex direction-col gap-8">
								<label for="collection-description" class="text-col-white"
									>Descripción (opcional)</label
								>
								<textarea
									id="collection-description"
									bind:value={newCollection.description}
									placeholder="Describe el propósito de esta colección..."
									class="bg-white"
								></textarea>
							</div>
							<div class="flex items-center gap-8">
								<input type="checkbox" id="is-public" bind:checked={newCollection.is_public} />
								<label for="is-public" class="text-col-white">Hacer pública</label>
							</div>
							<div class="flex gap-16">
								<button type="submit" class="btn primary bg-white text-col-1">
									<i class="las la-check"></i> Crear Colección
								</button>
								<button
									type="button"
									class="btn ghost text-col-white"
									onclick={() => (showCreateForm = false)}
								>
									Cancelar
								</button>
							</div>
						</form>
					</div>
				{/if}

				<!-- Grid de colecciones -->
				{#if loadingCollections}
					<div class="flex-center" style="min-height: 200px;">
						<RotatingNutriplan />
					</div>
				{:else if errorCollections}
					<div class="card pad-20 bg-gradient-leaf">
						<div class="flex-center direction-col gap-16">
							<i class="las la-exclamation-triangle" style="font-size: 3rem; color: white;"></i>
							<p class="text-col-white">Error: {errorCollections}</p>
							<button class="btn ghost text-col-white" onclick={fetchCollections}>Reintentar</button
							>
						</div>
					</div>
				{:else if collections.length === 0}
					<div class="card pad-20 text-center bg-gradient-mint">
						<i
							class="las la-folder-open"
							style="font-size: 4rem; color: white; margin-bottom: 1rem;"
						></i>
						<h3 class="h3 bold text-col-white mb-s">No tienes colecciones aún</h3>
						<p class="text-col-white mb">
							Crea tu primera colección para organizar tus recetas favoritas
						</p>
						<button class="btn primary bg-white text-col-1" onclick={() => (showCreateForm = true)}>
							<i class="las la-plus"></i> Crear mi primera colección
						</button>
					</div>
				{:else}
					<div class="grid regrid-cols-3 gap-24">
						{#each collections as collection}
							<CollectionCard
								{collection}
								showActions={true}
								onEdit={(collection) => console.log('Edit collection:', collection)}
								onDelete={deleteCollection}
							/>
						{/each}
					</div>
				{/if}
			</div>
		</section>

		<!-- Account Section -->
		<section class="section">
			<div class="container">
				<div class="grid regrid-cols-2 gap-24">
					<article class="card pad-20">
						<div class="flex justify-between items-center mb">
							<h2 class="h2 bold text-col-1">Datos de cuenta</h2>
							{#if !showEditProfile}
								<!-- <button class="btn ghost" onclick={startEditProfile}>
									<i class="las la-edit"></i> Editar
								</button> -->
							{/if}
						</div>

						{#if loadingProfile}
							<div class="flex-center">
								<RotatingNutriplan />
							</div>
						{:else if showEditProfile}
							<form
								onsubmit={(e) => {
									e.preventDefault();
									saveProfile();
								}}
								class="flex direction-col gap-16"
							>
								<div class="flex direction-col gap-8">
									<label for="email">Correo electrónico</label>
									<input
										id="email"
										type="email"
										value={userProfile?.email || $authUser?.email || ''}
										readonly
									/>
								</div>
								<div class="flex direction-col gap-8">
									<label for="first-name">Nombre</label>
									<input
										id="first-name"
										type="text"
										bind:value={editingProfile.first_name}
										placeholder="Tu nombre"
									/>
								</div>
								<div class="flex direction-col gap-8">
									<label for="last-name">Apellido</label>
									<input
										id="last-name"
										type="text"
										bind:value={editingProfile.last_name}
										placeholder="Tu apellido"
									/>
								</div>
								<div class="flex direction-col gap-8">
									<label for="phone">Teléfono</label>
									<input
										id="phone"
										type="tel"
										bind:value={editingProfile.phone_number}
										placeholder="Tu número de teléfono"
									/>
								</div>
								<div class="flex gap-16">
									<button type="submit" class="btn primary">
										<i class="las la-check"></i> Guardar cambios
									</button>
									<button type="button" class="btn ghost" onclick={cancelEditProfile}>
										Cancelar
									</button>
								</div>
							</form>
						{:else}
							<div class="flex direction-col gap-16">
								<div class="flex direction-col gap-8">
									<span class="text-col-2">Correo electrónico</span>
									<div class="info-value">{userProfile?.email || $authUser?.email || ''}</div>
								</div>
								<div class="flex direction-col gap-8">
									<span class="text-col-2">Nombre completo</span>
									<div class="info-value">
										{userProfile?.first_name || $authUser?.first_name || 'No especificado'}
										{userProfile?.last_name || $authUser?.last_name || ''}
									</div>
								</div>
								<div class="flex direction-col gap-8">
									<span class="text-col-2">Teléfono</span>
									<div class="info-value">{userProfile?.phone_number || 'No registrado'}</div>
								</div>
								<div class="flex justify-between items-center mt">
									<span class="sm-p text-col-2">Miembro desde 2025</span>
									<!-- <button class="btn ghost" type="button">
										<i class="las la-key"></i> Cambiar contraseña
									</button> -->
								</div>
							</div>
						{/if}
					</article>

					<article class="card pad-20 bg-gradient-leaf">
						<h2 class="h2 bold text-col-white mb">Información personal</h2>
						<div class="flex direction-col gap-16">
							<div class="info-item">
								<div class="info-label text-col-white p-ghost">Nombre completo</div>
								<div class="info-value text-col-white">
									{userProfile?.first_name || $authUser?.first_name || 'No especificado'}
									{userProfile?.last_name || $authUser?.last_name || ''}
								</div>
							</div>
							<div class="info-item">
								<div class="info-label text-col-white p-ghost">ID de usuario</div>
								<div class="info-value text-col-white">
									{userProfile?.id || $authUser?.id || 'N/A'}
								</div>
							</div>
							<div class="info-item">
								<div class="info-label text-col-white p-ghost">Estado de cuenta</div>
								<div class="info-value">
									<span class="chip bg-white" style="opacity: 100%; background-color: white;"
										>Activa</span
									>
								</div>
							</div>
						</div>
					</article>
				</div>
			</div>
		</section>
	</main>
{:else}
	<div class="flex-center" style="height: calc(100vh - 75px);">
		<RotatingNutriplan />
	</div>
{/if}

<style>
	.profile {
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	.hero-gradient {
		background: linear-gradient(
			135deg,
			var(--color-primary-dark) 0%,
			var(--color-primary-darker) 100%
		);
	}

	.hero-card {
		background: rgba(255, 255, 255, 0.95);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
	}

	.user-header {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.avatar {
		width: 60px;
		height: 60px;
		border-radius: 50%;
		background: var(--gradient-leaf);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.5rem;
		color: white;
	}

	.user-stats {
		display: flex;
		gap: 2rem;
		padding: 1rem;
		background: rgba(255, 255, 255, 0.1);
		border-radius: var(--radius-md);
		backdrop-filter: blur(5px);
	}

	.stat-item {
		text-align: center;
	}

	.stat-number {
		font-size: 1.5rem;
		font-weight: 700;
		color: white;
	}

	.stat-label {
		font-size: 0.85rem;
		color: rgba(255, 255, 255, 0.8);
	}

	.bg-gradient-mint {
		background: var(--gradient-mint);
	}

	.bg-gradient-sunrise {
		background: var(--gradient-sunrise);
	}

	.bg-gradient-leaf {
		background: var(--gradient-leaf);
	}

	.info-item {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.info-label {
		font-size: 0.85rem;
		font-weight: 600;
	}

	.info-value {
		font-weight: 600;
	}

	@media (max-width: 640px) {
		.user-header {
			flex-direction: column;
			text-align: center;
		}

		.user-stats {
			justify-content: center;
		}

		.profile .flex.wrap {
			flex-direction: column;
		}
	}
</style>
