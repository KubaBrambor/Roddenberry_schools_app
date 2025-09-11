export interface GeoLocation {
    latitude: number;
    longitude: number;
  }

  export interface EntityType {
    "@id"?: string;
    "@type"?: string;
    id: number;
    nazwa: string;
  }
  
  export interface Institution {
    "@id": string;
    "@type": string;
    nazwa: string;
    typ: EntityType;
    geolokalizacja: GeoLocation;
  }
  
  export interface RspoResponse {
    "@context": string;
    "@id": string;
    "@type": string;
    "hydra:member": Institution[];
  }

  export interface School {
    name: string;
    type: string;
    lat: number;
    lon: number;
    value: number;
  }