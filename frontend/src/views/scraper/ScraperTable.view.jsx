import { useSelector, useDispatch } from 'react-redux'
import { 
  fetchCurrencies, 
  onUpdateScraper, 
  onDeleteScraper, 
  deleteCurrency,
} from '../../store/actions'
import React from 'react'


const renderRowsTable = (scrapers, dispatch) => {
  if (!scrapers.length){
    return (
      <tr>
        <td colSpan="6" style={{textAlign:'center'}}>No data</td>
      </tr>
    )
  }
  console.log({scrapers})
  return scrapers.map(scraper => {
    return (
      <tr key={scraper.id}>
        <td>{scraper.id}</td>
        <td>{scraper.currency}</td>
        <td>{scraper.value}</td>
        <td>{scraper.frequency}</td>
        <td>{scraper.created_at}</td>
        <td>
            <button onClick={() => dispatch(onUpdateScraper(scraper.id))}>Editar</button>
            <button onClick={() => dispatch(deleteCurrency(scraper.id))}>Eliminar</button>
        </td>
      </tr>
    )
  })
}

const ScraperTable = (props) => {
  const scrapers = useSelector(state => Object.values(state.scraper.scrapers))
  const loaded = useSelector(state => state.scraper.loaded)
  const dispatch = useDispatch()
  if(!loaded) dispatch(fetchCurrencies())
  return (
    // Edit this as you like!
    <table className="table table-striped">
      <thead>
        <th>ID</th>
        <th>Moneda</th>
        <th>Último valor leído</th>
        <th>Frecuencia (seg)</th>
        <th>Fecha de creación</th>
        <th>Acciones</th>
      </thead>
      <tbody>{renderRowsTable(scrapers, dispatch)}</tbody>
    </table>
     
  )
}

export default ScraperTable