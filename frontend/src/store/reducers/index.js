import { 
  FETCH_SCRAPERS,
  CREATE_SCRAPER,
  DELETE_SCRAPER,
  UPDATE_SCRAPER,
  ON_UPDATE_SCRAPER,
  ON_DELETE_SCRAPER,
  SET_CURRENCY,
  SET_FREQUENCY,
  ON_ERROR_SCRAPER,
} from '../actions/constants';

const initialState = {
  scrapers: {},
  msg: '',
  loaded: false,
  scraper: {
    mode:'create',
    id: null,
    currency: '',
    frequency: null
  }
}

export default (state = initialState, action) => {

  switch (action.type){
    case ON_ERROR_SCRAPER:
      return {
        ...state,
        msg: action.payload
      }
    case FETCH_SCRAPERS:
      return {
        ...state, 
        scrapers: action.payload,
        loaded: true
      }
    case SET_CURRENCY:
      return {
        ...state,
        scraper: { ...state.scraper, currency: action.payload}
      }
      case SET_FREQUENCY:
      return {
        ...state,
        scraper: { ...state.scraper, frequency: Number(action.payload)}
      }
    case CREATE_SCRAPER:
      return {
        ...state,
        scrapers: {
          ...state.scrapers,
          [action.payload.id]: action.payload
        }
      }
    case ON_DELETE_SCRAPER:
      return {
        ...state,
        scraper: { 
            ...initialState.scraper,
            mode: 'delete', 
            id: action.payload
          }
      }
    case DELETE_SCRAPER:
    const { [action.payload.currencyId]: deleted, ...rest } = state.scrapers
      return {
        ...state,
        scrapers: rest,
        scraper: {
          ...initialState.scraper
        }
      }
    case ON_UPDATE_SCRAPER:
      return {
        ...state,
        scraper: { 
          mode: 'edit', 
            ...state.scrapers[action.payload] 
          }
      }
    case UPDATE_SCRAPER:
      return {
        ...state,
        scrapers: {
          ...state.scrapers,
          [action.payload.data.id]: action.payload.data
        },
        scraper: {
          ...initialState.scraper,
          frequency: null,
        }
      }
  
    default:
        return state
  }
  
}