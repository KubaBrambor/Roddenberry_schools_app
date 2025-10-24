/**
 * TypeScript types for school-related data models
 * These types correspond to the backend Python models in app.models.schools
 * Types were generated using a opeanapi-typescript generator
 */
import type { components } from "./api"

type schemas = components["schemas"]

export type SzkolaPublicShort = schemas["SzkolaPublicShort"]
export type SzkolaPublicWithRelations = schemas["SzkolaPublicWithRelations"]
export type TypSzkolyPublic = schemas["TypSzkolyPublic"]

export type SzkolaPublicShortFromGeoJsonFeatures = Omit<
    SzkolaPublicShort,
    "typ" | "status_publicznoprawny"
> & {
    typ: string
    status_publicznoprawny: string
}

export type WynikE8PublicWithPrzedmiot = schemas["WynikE8PublicWithPrzedmiot"]
export type WynikEMPublicWithPrzedmiot = schemas["WynikEMPublicWithPrzedmiot"]
