import AveragesChart from "../components/charts/AveragesChart"
import OverTimeChart from "../components/charts/OverTimeChart"
import CorrelationHeatMap from "../components/charts/CorrelationHeatMap"
import BestValueCard from "../components/cards/BestValueCard"
import PriceCategoryChart from "../components/charts/PriceCategoryChart"

export default function HomePage() {
  return (
    <main style={{ padding: '2rem' }}>
      <h1>King County Housing Dashboard</h1>
      <OverTimeChart compact={true} />
      <AveragesChart compact={true}/>
      <CorrelationHeatMap compact={true}/>
      <PriceCategoryChart compact={true}/>
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