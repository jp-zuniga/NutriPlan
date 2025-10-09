import { SESSION_ACCESS_COOKIE } from '$lib/cookies';
import { API_ME_ENDPOINT } from '$lib/endpoints';

export const GET = async ({ cookies, fetch }) => {
  const access = cookies.get(SESSION_ACCESS_COOKIE);
  if (!access) {
    return new Response(JSON.stringify({ error: 'No hay sesión activa' }), { status: 401 });
  }

  try {
    const response = await fetch(API_ME_ENDPOINT, {
      method: 'GET',
      headers: { Authorization: `Bearer ${access}` }
    });

    if (!response.ok) {
      return new Response(
        JSON.stringify({ error: `Error obteniendo perfil (HTTP ${response.status})` }),
        { status: response.status }
      );
    }

    const data = await response.json();
    return new Response(JSON.stringify(data), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: `Hubo un error: ${err}` }), { status: 500 });
  }
};

