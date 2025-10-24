// Voivodeships mapping file
// Export a constant containing mappings of voivodeship keys to their respective names and bounding boxes
// later on we can use nominatim API from openstreetmap to get this data

import type { VoivodeshipData } from "~/types/voivodeships"

/**
 * Mapping of voivodeship keys to their respective data including Polish names and bounding boxes
 * Bounding boxes are in bbox format (min_lng, min_lat, max_lng, max_lat) and are approximate extents
 */
export const VOIVODESHIP_NAMES: Record<string, VoivodeshipData> = {
    dolnoslaskie: {
        name: "Dolnośląskie",
        coordinates: {
            min_lng: 14.76,
            min_lat: 49.98,
            max_lng: 17.91,
            max_lat: 51.91,
        },
    },
    kujawsko_pomorskie: {
        name: "Kujawsko-pomorskie",
        coordinates: {
            min_lng: 17.16,
            min_lat: 52.28,
            max_lng: 19.88,
            max_lat: 53.83,
        },
    },
    lubelskie: {
        name: "Lubelskie",
        coordinates: {
            min_lng: 21.52,
            min_lat: 50.2,
            max_lng: 24.25,
            max_lat: 52.35,
        },
    },
    lubuskie: {
        name: "Lubuskie",
        coordinates: {
            min_lng: 14.4,
            min_lat: 51.33,
            max_lng: 16.6,
            max_lat: 53.18,
        },
    },
    lodzkie: {
        name: "Łódzkie",
        coordinates: {
            min_lng: 17.95,
            min_lat: 50.78,
            max_lng: 20.75,
            max_lat: 52.45,
        },
    },
    malopolskie: {
        name: "Małopolskie",
        coordinates: {
            min_lng: 18.92,
            min_lat: 49.07,
            max_lng: 21.55,
            max_lat: 50.59,
        },
    },
    mazowieckie: {
        name: "Mazowieckie",
        coordinates: {
            min_lng: 19.15,
            min_lat: 50.95,
            max_lng: 23.25,
            max_lat: 53.55,
        },
    },
    opolskie: {
        name: "Opolskie",
        coordinates: {
            min_lng: 16.8461,
            min_lat: 49.942,
            max_lng: 18.8073,
            max_lat: 51.2778,
        },
    },
    podkarpackie: {
        name: "Podkarpackie",
        coordinates: {
            min_lng: 21.03,
            min_lat: 48.95,
            max_lng: 23.66,
            max_lat: 50.9,
        },
    },
    podlaskie: {
        name: "Podlaskie",
        coordinates: {
            min_lng: 21.45,
            min_lat: 52.17,
            max_lng: 24.1,
            max_lat: 54.5,
        },
    },
    pomorskie: {
        name: "Pomorskie",
        coordinates: {
            min_lng: 16.65,
            min_lat: 53.4,
            max_lng: 19.75,
            max_lat: 54.92,
        },
    },
    slaskie: {
        name: "Śląskie",
        coordinates: {
            min_lng: 17.8872,
            min_lat: 49.2956,
            max_lng: 20.0559,
            max_lat: 51.1617,
        },
    },
    swietokrzyskie: {
        name: "Świętokrzyskie",
        coordinates: {
            min_lng: 19.6,
            min_lat: 50.1,
            max_lng: 22.0,
            max_lat: 51.4,
        },
    },
    "warminsko-mazurskie": {
        name: "Warmińsko-mazurskie",
        coordinates: {
            min_lng: 19.05,
            min_lat: 53.07,
            max_lng: 22.95,
            max_lat: 54.52,
        },
    },
    wielkopolskie: {
        name: "Wielkopolskie",
        coordinates: {
            min_lng: 15.68,
            min_lat: 51.05,
            max_lng: 19.19,
            max_lat: 53.7,
        },
    },
    "zachodnio-pomorskie": {
        name: "Zachodniopomorskie",
        coordinates: {
            min_lng: 13.95,
            min_lat: 52.58,
            max_lng: 17.1,
            max_lat: 54.65,
        },
    },
}
