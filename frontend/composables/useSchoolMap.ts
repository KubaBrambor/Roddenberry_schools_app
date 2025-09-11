import { ref } from 'vue';
import maplibregl from 'maplibre-gl';
import { useMapUtils } from '~/composables/useMapUtils';
import type { School } from '~/types/rspo';

export const useSchoolMap = () => {

    const mapInstance = ref<maplibregl.Map | null>(null);
    const { getColorForValue, getShapeSVG } = useMapUtils();

    const initializeMap = (containerId: string, schools: School[]) => {
        if (mapInstance.value || !schools.length) return;

        console.log("Inicjalizacja mapy z", schools.length, "szkołami");
        
        const map = new maplibregl.Map({
            container: containerId,
            style: "https://tiles.openfreemap.org/styles/liberty",
            center: [19.5, 52.2],
            zoom: 6.5,
            attributionControl: false 
        });

        map.addControl(new maplibregl.NavigationControl(), 'top-right');
        map.addControl(new maplibregl.FullscreenControl(), 'top-right');

        map.on('load', () => {
            schools.forEach((school) => {
                const el = document.createElement("div");
                const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                svg.setAttribute("viewBox", "0 0 24 24");
                svg.setAttribute("width", "24");
                svg.setAttribute("height", "24");
                svg.innerHTML = getShapeSVG(school.type);
                el.appendChild(svg);
                el.style.color = getColorForValue(school.value);
                el.style.width = "24px";
                el.style.height = "24px";
                el.style.cursor = 'pointer';
                el.title = school.name;
                
                new maplibregl.Marker({ element: el })
                    .setLngLat([school.lon, school.lat])
                    .setPopup(
                      new maplibregl.Popup({ offset: 25 })
                        .setHTML(`<h3>${school.name}</h3><p>Typ: ${school.type}<br>Wartość: ${school.value}</p>`)
                    )
                    .addTo(map);
            });
        });

        mapInstance.value = map;
    };

    return { initializeMap };
};