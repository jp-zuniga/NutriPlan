import { writable } from "svelte/store";
import { Receta } from "$lib/classes/receta";

export const initialRecipes = writable([
  new Receta(
    1,
    "Ensalada César",
    "Una ensalada fresca con lechuga romana, aderezo cremoso, crutones y queso parmesano.",
    "15 min",
    320,
    4.5,
    128,
    300,
    ["rápida", "saludable", "vegetariana"],
    "https://www.gourmet.cl/wp-content/uploads/2016/09/EnsaladaCesar2.webp"
  ),
  new Receta(
    2,
    "Spaghetti Boloñesa",
    "Clásico plato italiano con salsa de tomate, carne molida y especias.",
    "40 min",
    650,
    4.7,
    256,
    510,
    ["italiana", "pastas", "casera"],
    "https://images.ctfassets.net/uexfe9h31g3m/6QtnhruEFi8qgEyYAICkyS/ab01e9b1da656f35dd1a721c810162a0/Spaghetti_bolognese_4x3_V2_LOW_RES.jpg?w=2000&h=2000&fm=webp&fit=thumb&q=100"
  ),
  new Receta(
    3,
    "Smoothie de Frutas",
    "Bebida refrescante y nutritiva con plátano, fresa y yogur.",
    "10 min",
    180,
    4.3,
    74,
    210,
    ["saludable", "desayuno", "vegano"],
    "https://www.vitamix.com/content/dam/vitamix/migration/media/recipe/rcpfruitsmoothie/images/fruitsmoothiejpg.jpg"
  ),
  new Receta(
    4,
    "Pollo al Horno",
    "Muslos de pollo horneados con especias, ajo y limón.",
    "55 min",
    520,
    4.8,
    340,
    670,
    ["alto en proteína", "sin gluten"],
    "https://cocinemosjuntos.com.co/media/mageplaza/blog/post/t/i/tips-para-preparar-pollo-al-horno-jugoso-y-perfecto_1_.jpg"
  ),
  new Receta(
    5,
    "Brownies de Chocolate",
    "Brownies suaves y esponjosos con intenso sabor a cacao.",
    "35 min",
    450,
    4.9,
    512,
    890,
    ["postre", "chocolate", "dulce"],
    "https://www.aceitesdeolivadeespana.com/wp-content/uploads/2019/03/brownies-de-chocolate.png"
  )
]);

