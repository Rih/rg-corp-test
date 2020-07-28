import React, { 
  //createContext, 
  //useContext, 
  //useReducer 
} from 'react'
import { useSelector, useDispatch } from 'react-redux'
import CardContainer from '../../components/CardContainer'
import TableContainer from '../../components/TableContainer'
import FormContainer from '../../components/FormContainer'
import InputContainer from '../../components/InputContainer'
import Input from '../../components/Input'
import ScraperTable from './ScraperTable.view'
import { 
  onSetFrequency, 
  onSetCurrency, 
  setCurrency, 
  updateCurrency,
  fetchCurrencies
} from '../../store/actions'
import { reduce } from 'lodash'


const onKeyFrequency = (event, dispatch) => {
  console.log({event})
  event.preventDefault()
  dispatch(onSetFrequency(event.target.value))
}

const onKeyCurrency = (event, dispatch) => {
  console.log({event})
  event.preventDefault()
  dispatch(onSetCurrency(event.target.value))
}

const setAverage = (scrapers) => {
  const scraperArray = Object.values(scrapers)
  const len = scraperArray.length
  if (len === 0) return 0
  const total = reduce(scraperArray, (acc, s) => acc + s.frequency, 0)
  return total / len
}
const ScraperView = (props) => {
  const scraper = useSelector(state => state.scraper.scraper)
  console.log({scraper})
  // const loaded = useSelector(state => state.scraper.loaded)
  const avgFrequency = setAverage(useSelector(state => state.scraper.scrapers))
  const msg = useSelector(state => state.scraper.msg)
  const dispatch = useDispatch()
  return (
    // Edit this as you like!
    <CardContainer 
        height='30vh' 
        width='50%' 
        margin='2rem auto' 
        padding='2rem' 
        justifyContent='center' 
        alignItems='center'
        flexDirection="column">
      <FormContainer className="container_form">
        <InputContainer  flexDirection="column">
          <InputContainer flexDirection="row">
            <InputContainer flexDirection="column">
              <label htmlFor="frequency">Frecuencia (segundos)</label>
              <Input type="number" id="frequency" name="frequency" onChange={(event) => onKeyFrequency(event, dispatch)} value={scraper.frequency} />
            </InputContainer>
            <InputContainer flexDirection="column">
              <label htmlFor="currency">Moneda</label>
              <Input id="currency" name="currency" onChange={(event) => onKeyCurrency(event, dispatch)} value={scraper.currency} />
            </InputContainer>
            <Input type="button" id="create" name="create" onClick={() => dispatch(setCurrency(scraper))} value="Crear" />
          </InputContainer>
          <hr />
          <InputContainer>
          <Input type="button" id="update" name="update" onClick={() => dispatch(updateCurrency(scraper))} value="Actualizar registro" />
          <Input type="button" id="refresh" name="refresh" onClick={() => dispatch(fetchCurrencies())} value="Actualizar" />
        </InputContainer>
        </InputContainer>
      </FormContainer>
      <span>{msg}</span>
      <TableContainer className="container_table">
          <ScraperTable />
      </TableContainer>
      <span>Frecuencia promedio: {avgFrequency}</span>
    </CardContainer>
  )
}

export default ScraperView