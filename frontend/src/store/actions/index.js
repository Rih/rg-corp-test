import  {
    fetchScrapers,
    createScraper,
    updateScraper,
    deleteScraper,
} from '../../api/scraperAPI';
import { 
    FETCH_SCRAPERS,
    CREATE_SCRAPER,
    DELETE_SCRAPER,
    UPDATE_SCRAPER,
    SET_CURRENCY,
    SET_FREQUENCY,
    ON_UPDATE_SCRAPER,
    ON_DELETE_SCRAPER,
    ON_ERROR_SCRAPER,
 } from './constants';
import { reduce } from 'lodash'

//static actions

export const onSetFrequency = (freq) => {
    return { type: SET_FREQUENCY, payload: freq }
}

export const onSetCurrency = (currency) => {
    return { type: SET_CURRENCY, payload: currency }
}

export const onUpdateScraper = (id) => {
    return { type: ON_UPDATE_SCRAPER, payload: id }
}

export const onDeleteScraper = (id) => {
    return { type: ON_DELETE_SCRAPER, payload: id }
}


// async actions

export const fetchCurrencies = (page = 1) => async dispatch => {
    const scrapers = await fetchScrapers()
    //convert list into object key by id
    console.log({fetch: scrapers})
    const response = reduce(scrapers.data, (acc, row) => ({...acc, [row.id]: {...row } }) , {})
    console.log({response})
    dispatch({type: FETCH_SCRAPERS, payload: response })
}


export const setCurrency = (data) => async dispatch => {
    try{
        const request = await createScraper(data)
        const response = request.data
        dispatch({type: CREATE_SCRAPER, payload: response })
    }catch(err){
        console.log({err})
        dispatch({type: ON_ERROR_SCRAPER, payload: err.response.data.error })
    }
    
}

export const updateCurrency = (data) => async dispatch => {
    try{
        const request = await updateScraper(data)
        const response = request.data
        dispatch({type: UPDATE_SCRAPER, payload: {data, response} })
    }catch(err){
        console.log({err})
        dispatch({type: ON_ERROR_SCRAPER, payload: err.response.data.error })
    }
}

export const deleteCurrency = (currencyId) => async dispatch => {
    try{
        const request = await deleteScraper(currencyId)
        const response = request.data
        dispatch({type: DELETE_SCRAPER, payload: {currencyId, response} })
    }catch(err){
        console.log({err})
        dispatch({type: ON_ERROR_SCRAPER, payload: err.response.data.error })
    }
}