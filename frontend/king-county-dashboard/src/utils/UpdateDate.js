
export default async function UpdateDate() {
    try {
        const res = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/`
        );
        if (!res.ok) {
          throw new Error("Network response was not ok" + res.statusText);
        }
        const data = await res.json();
        const date = data[0].date;
        return date;
    } catch (error) {
        console.error("Error fetching update date:", error);
        return "Unknown";
    }

}