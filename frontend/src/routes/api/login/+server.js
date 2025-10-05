import { NODE_ENV } from "$env/static/private";
import { SESSION_ACCESS_COOKIE } from "$lib/cookies";
import { API_LOGIN_ENDPOINT } from "$lib/endpoints";

export const POST = async({ request, cookies }) => {
    let payload
    try {
        payload = await request.json();
        // console.log("Payload: ", payload)
    } catch {
        return new Response(JSON.stringify({ error: 'Body inválido' }), { status: 400 });
    }

    try {
        console.log("Request to " + API_LOGIN_ENDPOINT + " with body:", payload)

        const upstream = await fetch(API_LOGIN_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }).catch((err) => {
            console.log("Communication error: ", err)
            return new Response(JSON.stringify({ errror: err }), { status: 500 })
        })

        console.log("Upstream: ", upstream)
        const data = await upstream.json();

        if(!upstream.ok) {
            const message = data?.message ?? `Error desconocido (HTTP ${upstream.status})`;
            return new Response(JSON.stringify({ error: message }), { status: upstream.status })
        }

        console.log("Data:", data)
        const access = data.access;
        console.log("Access:", access)

        if(!access) {
            return new Response(JSON.stringify({ error: 'Respuesta invalida del servidor de autentificación' }), { status: 500 })
        }

        cookies.set(SESSION_ACCESS_COOKIE, access, {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            secure: NODE_ENV == 'production',
            maxAge: 60 * 60 // 1h
        });

        return new Response(JSON.stringify({ok: true}), {status: 200})
    } catch(err) {
        return new Response(JSON.stringify({ error: err }), { status: 500 })
    }
}