import { goto } from "$app/navigation";
const search_path = "/search/";

export function gotoSearch(search_term: string): void {
  goto(search_path + search_term.replaceAll(' ', '-').toLowerCase());
}