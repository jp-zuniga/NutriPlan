import { goto } from "$app/navigation";
const search_path = "/search/";

export function gotoSearch(search_term: String): void {
  goto(search_path + search_term.replaceAll(' ', '-').toLowerCase());
}