import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Items from "./components/Items";
import Filters from './components/Filters';
import ProductPage from './components/ProductPage';
import Pagination from './components/Pagination';

class App extends React.Component {
  state = {
    items: [],
    search: '',
    filters: {
      brand: '',
      color: '',
      kind: '',
      priceMin: '',
      priceMax: '',
      ordering: '',
    },
    page: 1,
    count: 0,
    next: null,
    previous: null,
  };

  componentDidMount() {
    this.loadFromURL();
  }

  loadFromURL = () => {
    const params = new URLSearchParams(window.location.search);
    const search = params.get('search') || '';
    const filters = {
      brand: params.get('brand') || '',
      color: params.get('color') || '',
      kind: params.get('kind') || '',
      priceMin: params.get('price_min') || '',
      priceMax: params.get('price_max') || '',
      ordering: params.get('ordering') || '',
    };
    const page = parseInt(params.get('page')) || 1;

    this.setState({ search, filters, page }, this.fetchItems);
  };

  updateURL = () => {
    const { search, filters, page } = this.state;
    const params = new URLSearchParams();

    if (search) params.set('search', search);
    if (filters.brand) params.set('brand', filters.brand);
    if (filters.color) params.set('color', filters.color);
    if (filters.kind) params.set('kind', filters.kind);
    if (filters.priceMin) params.set('price_min', filters.priceMin);
    if (filters.priceMax) params.set('price_max', filters.priceMax);
    if (filters.ordering) params.set('ordering', filters.ordering);
    if (page && page > 1) params.set('page', page);

    const newURL = `${window.location.pathname}?${params.toString()}`;
    window.history.pushState(null, '', newURL);
  };

  fetchItems = () => {
    const { search, filters, page } = this.state;
    const params = new URLSearchParams();

    if (search) params.set('search', search);
    if (filters.brand) params.set('brand', filters.brand);
    if (filters.color) params.set('color', filters.color);
    if (filters.kind) params.set('kind', filters.kind);
    if (filters.priceMin) params.set('price_min', filters.priceMin);
    if (filters.priceMax) params.set('price_max', filters.priceMax);
    if (filters.ordering) params.set('ordering', filters.ordering);
    if (page) params.set('page', page);

    fetch(`http://127.0.0.1:8000/api/products/?${params.toString()}`)
      .then(res => res.json())
      .then(data => this.setState({
        items: data.results,
        count: data.count,
        next: data.next,
        previous: data.previous,
      }))
      .catch(console.error);

    this.updateURL();
  };

  handleSearch = (searchText) => {
    this.setState({ search: searchText, page: 1 }, this.fetchItems);
  };

  handleFilterApply = (filters) => {
    this.setState({ filters, page: 1 }, this.fetchItems);
  };

  handlePageChange = (newPage) => {
    this.setState({ page: newPage }, this.fetchItems);
  };

  render() {
    const { items, page, next, previous, count } = this.state;
    const totalPages = Math.ceil(count / 50);

    return (
      <Router>
        <div className="wrapper">
          <Header onSearch={this.handleSearch} searchValue={this.state.search} />
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <Filters
                    onApply={this.handleFilterApply}
                    currentFilters={this.state.filters}
                  />
                  <Items items={items} />

                  <Pagination
                    page={page}
                    totalPages={totalPages}
                    onPageChange={this.handlePageChange}
                  />
                </>
              }
            />
            <Route path="/product/:id" element={<ProductPage />} />
          </Routes>
          <Footer />
        </div>
      </Router>
    );
  }
}


export default App;
