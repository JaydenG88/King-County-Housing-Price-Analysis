
export default async function Regions() {

      try {
        const res = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/regions`
        );
        if (!res.ok) throw new Error("Network response was not ok");
        const regionsData = await res.json();
        return regionsData;
      } catch (error) {
        console.error("Error fetching regions:", error);
        return [];
      }
    }

