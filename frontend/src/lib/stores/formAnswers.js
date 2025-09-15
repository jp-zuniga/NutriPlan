import { writable } from 'svelte/store';

export const formAnswers = writable({
  foodAnswers: [],
  medicalAnswers: []
});
