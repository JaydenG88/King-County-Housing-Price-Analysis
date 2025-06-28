import AveragesChart from "./components/AveragesChart"
import OverTimeChart from "./components/OverTimeChart"
import CorrelationHeatMap from "./components/CorrelationHeatMap"
import BestValueCard from "./components/BestValueCard"
import PriceCategoryChart from "./components/PriceCategoryChart"

export default function HomePage() {
  return (
    <main style={{ padding: '2rem' }}>
      <h1>King County Housing Dashboard</h1>
      <OverTimeChart metric="price" type="mean" region="King County" />
      <AveragesChart metric="price" type="mean" region="King County"/>
      <CorrelationHeatMap />
      <PriceCategoryChart />
      <BestValueCard  
        sqft={1500}
        price={500000}
        zip="98001"
        city="Seattle"
        state="WA"
        street_address="123 Main St"
        bedrooms={3}
        bathrooms={2}
        url="https://example.com/listing/123"
        image="https://ssl.cdn-redfin.com/photo/1/islphoto/754/genIslnoResize.2381754_0.jpg"
        price_per_sqft={333.33}
        price_category="Low"
      
      />
    </main>
  )
}