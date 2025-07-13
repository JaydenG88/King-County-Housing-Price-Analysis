
export default function Regions() {

    async function fetchRegions() {
      try {
        const res = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/regions`
        );
        if (!res.ok) throw new Error("Network response was not ok");
        const regionsData = await res.json();
        setRegions(regionsData);
      } catch (error) {
        setError(error);
      }
    }

    return fetchRegions().then((regions) => {
        return regions;
    }).catch((error) => {
        console.error("Error fetching regions:", error);
        return [];
    });

}