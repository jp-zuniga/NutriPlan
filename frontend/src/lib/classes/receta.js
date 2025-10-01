export class Receta {
  constructor(id, titulo, descripcion, tiempo_preparacion, calorias, rating, reviews, likes, badges, imagen)
  {
    this.id = id;
    this.titulo = titulo;
    this.descripcion = descripcion;
    this.tiempo_preparacion = tiempo_preparacion;
    this.calorias = calorias;
    this.rating = rating;
    this.reviews = reviews;
    this.likes = likes;
    this.badges = badges;
    this.imagen = imagen;
  }
}

export function obtenerRecetaPorID(recetas, id) {
  for(let receta of recetas) {
    if(receta.id == id)
      return receta;
  }
  return null;
}