let allData = [];

// Category mappings - using short names that match the CSV columns
const categories = {
    'Broad': ['N50', 'NN50', 'N100', 'N200', 'NTOTLM', 'N500', 'NMC5025', 'N500EQ', 'NMC150', 'NMC50', 'NMCSEL', 'NMC100', 'NSC250', 'NSC50', 'NSC100', 'NMICRO', 'NLMC250', 'NMSC400', 'NT10EWT', 'NT15EWT', 'NT20EWT', 'N50EQWGT', 'NIFTY500 EQUAL WEIGHT.1'],
    'Sector': ['NAUTO', 'NBANK', 'NCHEM', 'NFINSERV', 'NFINS2550', 'NFINSXB', 'NFMCG', 'NHEALTH', 'NTECH', 'NMEDIA', 'NMETAL', 'NPHARMA', 'NPVTBANK', 'NPSUBANK', 'NREALTY', 'NCONDUR', 'NOILGAS', 'NMSFINS', 'NMSHC', 'NMSITT', 'NCAPMRKT', 'NCOMM', 'NSERVSEC'],
    'Strategy': ['N100EWT', 'N100LV30', 'N200M30', 'N200AL30', 'N100AL30', 'NAL50', 'NALV30', 'NAQLV30', 'NAQVLV30', 'NDIVOP50', 'NLV50', 'NHBET50', 'NGROW15', 'N100QL30', 'N200QL30', 'NQLLV30', 'N500QL50', 'N500M50', 'N500LV50', 'N500V50', 'N500MQLV', 'N500MQ50', 'N50V20', 'N200V30', 'NMC150M50', 'NMC150Q', 'N500FQ30', 'NSC250Q', 'NMSCMQ', 'NSC250MQ', 'N100LIQ15', 'NMCL15', 'N50SH', 'N500SH', 'NSH25'],
    'Thematic': ['NICON', 'NIDEF', 'NIDIGI', 'NIIL', 'NIMFG', 'NCPSE', 'NENRGY', 'NEVNAA', 'NHOUS', 'N100ESG', 'N100ESGE', 'N100ESGSL', 'NINFRA', 'NTOUR', 'NINACON', 'NCHOUS', 'NMSICON', 'NMOBIL', 'NNCCON', 'NRURAL', 'NTRANS', 'NIINT', 'NPSE', 'NMNC', 'NREIT', 'NIPO', 'NSMEE', 'NIRLPSU', 'NBIRLA', 'NMAHIN', 'NTATA', 'NTATA25', 'NMAATR', 'NMF5032', 'NINF5032', 'NWAVES', 'DSPQ', 'DSP ELSS', 'KBIK CON', 'KBIK GOLD', 'AXISINVE', 'UTI FLEX', 'ICICI SIL', 'N10YRGS', 'NIFTY 10 YR BENCHMARK G-SEC.1']
};

// Get the base path from the current location
const pathParts = window.location.pathname.split('/').filter(Boolean);
let basePath = '';
if (pathParts.length > 0) {
    const firstPath = pathParts[0].toLowerCase();
    if (firstPath === 'risk-reward' || firstPath === 'riskreward') {
        basePath = '/' + pathParts[0]; // Use the actual case from URL
    }
}

async function loadData() {
    const loading = document.getElementById('loading');
    const container = document.getElementById('data-table-container');
    const duration = document.getElementById('duration').value;

    try {
        loading.textContent = 'Loading data...';
        loading.classList.remove('hidden');
        container.classList.add('hidden');
        
        console.log('Fetching data for duration:', duration);
        const res = await fetch(`${basePath}/api/metrics?duration=${duration}`);
        if (!res.ok) throw new Error('Failed to fetch data');
        
        allData = await res.json();
        console.log('Data loaded:', allData.length, 'items');
        
        loading.classList.add('hidden');
        container.classList.remove('hidden');
        
        renderTable(allData);
    } catch (err) {
        loading.textContent = 'Failed to load data: ' + err.message;
        console.error(err);
    }
}

function renderTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';
    
    // Create a map for quick lookup
    const dataMap = {};
    data.forEach(item => {
        dataMap[item['Index Name']] = item;
    });
    
    // Find max row count
    let maxRows = 0;
    Object.keys(categories).forEach(cat => {
        maxRows = Math.max(maxRows, categories[cat].length);
    });
    
    // Build rows
    for (let i = 0; i < maxRows; i++) {
        const tr = document.createElement('tr');
        
        Object.keys(categories).forEach(category => {
            const td = document.createElement('td');
            const indexName = categories[category][i];
            
            if (indexName && dataMap[indexName]) {
                const item = dataMap[indexName];
                
                const indexRow = document.createElement('div');
                indexRow.className = 'index-row';
                
                const nameCell = document.createElement('div');
                nameCell.className = 'index-name-cell';
                nameCell.textContent = indexName;
                nameCell.title = indexName;
                nameCell.onclick = () => showDetails(item);
                
                const metricsGrid = document.createElement('div');
                metricsGrid.className = 'metrics-grid';
                
                // Ret
                const retCell = createMetricCell(item.Ret, 'ret', 'Return');
                // Risk
                const riskCell = createMetricCell(item.Risk, 'risk', 'Risk');
                // V1
                const v1Cell = createMetricCell(item.V1, 'v1', 'V1');
                // RMom
                const rmomCell = createMetricCell(item.RMom, 'rmom', 'Relative Momentum');
                
                metricsGrid.appendChild(retCell);
                metricsGrid.appendChild(riskCell);
                metricsGrid.appendChild(v1Cell);
                metricsGrid.appendChild(rmomCell);
                
                indexRow.appendChild(nameCell);
                indexRow.appendChild(metricsGrid);
                td.appendChild(indexRow);
            }
            
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    }
}

function createMetricCell(value, type, label) {
    const cell = document.createElement('div');
    cell.className = `metric-cell ${getColorClass(value, type)}`;
    cell.textContent = value;
    cell.setAttribute('data-tooltip', `${label}: ${value}`);
    return cell;
}

function getColorClass(value, type) {
    if (type === 'rmom') {
        // RMom: 80-100 is GREEN (best), 10-20 is RED (worst)
        if (value === null || value === undefined) return '';
        if (value >= 80) return 'green-dark';
        if (value >= 60) return 'light-green';
        if (value >= 40) return 'yellow';
        if (value >= 20) return 'orange';
        return 'red';
    }
    
    if (type === 'ret') {
        // Return: Higher is better (green), lower is worse (red)
        if (value >= 20) return 'green-dark';
        if (value >= 15) return 'light-green';
        if (value >= 10) return 'yellow';
        if (value >= 5) return 'orange';
        return 'red';
    } else if (type === 'v1') {
        // V1 (Percentile): Higher is better (1 = best, 0 = worst)
        if (value === null || value === undefined) return '';
        if (value >= 0.8) return 'green-dark';
        if (value >= 0.6) return 'light-green';
        if (value >= 0.4) return 'yellow';
        if (value >= 0.2) return 'orange';
        return 'red';
    } else if (type === 'risk') {
        // Risk: 80-100 is GREEN (best), 10-20 is RED (worst)
        if (value >= 80) return 'green-dark';
        if (value >= 60) return 'light-green';
        if (value >= 40) return 'yellow';
        if (value >= 20) return 'orange';
        return 'red';
    }
    return '';
}

function showDetails(item) {
    // Navigate to heatmap page
    window.location.href = `${basePath}/heatmap?index=${encodeURIComponent(item['Index Name'])}`;
}

function viewCategoryHeatmap(category) {
    // Navigate to heatmap page for entire category
    window.location.href = `${basePath}/heatmap?category=${encodeURIComponent(category)}`;
}

window.viewCategoryHeatmap = viewCategoryHeatmap;

// Sorting state
const sortState = {
    'Broad': { metric: null, ascending: true },
    'Sector': { metric: null, ascending: true },
    'Strategy': { metric: null, ascending: true },
    'Thematic': { metric: null, ascending: true }
};

function sortCategory(category, metric) {
    // Toggle sort direction if clicking same metric
    if (sortState[category].metric === metric) {
        sortState[category].ascending = !sortState[category].ascending;
    } else {
        sortState[category].metric = metric;
        sortState[category].ascending = false; // Start with descending for better UX
    }
    
    // Create a map for quick lookup
    const dataMap = {};
    allData.forEach(item => {
        dataMap[item['Index Name']] = item;
    });
    
    // Sort the category indices
    const sorted = [...categories[category]].sort((a, b) => {
        const itemA = dataMap[a];
        const itemB = dataMap[b];
        
        if (!itemA || !itemB) return 0;
        
        let valA, valB;
        
        if (metric === 'name') {
            valA = a;
            valB = b;
            return sortState[category].ascending 
                ? valA.localeCompare(valB)
                : valB.localeCompare(valA);
        } else if (metric === 'ret') {
            valA = itemA.Ret;
            valB = itemB.Ret;
        } else if (metric === 'v1') {
            valA = itemA.V1 !== null ? itemA.V1 : -1;
            valB = itemB.V1 !== null ? itemB.V1 : -1;
        } else if (metric === 'risk') {
            valA = itemA.Risk;
            valB = itemB.Risk;
        } else if (metric === 'rmom') {
            valA = itemA.RMom !== null ? itemA.RMom : 999;
            valB = itemB.RMom !== null ? itemB.RMom : 999;
        }
        
        return sortState[category].ascending 
            ? valA - valB
            : valB - valA;
    });
    
    // Update the categories object
    categories[category] = sorted;
    
    // Re-render the table
    renderTable(allData);
}

window.sortCategory = sortCategory;

function searchIndices() {
    const searchBox = document.getElementById('search-box');
    const searchTerm = searchBox.value.toLowerCase().trim();
    
    // Get all index rows across all categories
    const allIndexRows = document.querySelectorAll('.index-row');
    
    allIndexRows.forEach(indexRow => {
        const nameCell = indexRow.querySelector('.index-name-cell');
        if (nameCell) {
            const indexName = nameCell.textContent.toLowerCase();
            
            // Show/hide index row based on search match
            if (searchTerm === '' || indexName.includes(searchTerm)) {
                indexRow.style.display = '';
            } else {
                indexRow.style.display = 'none';
            }
        }
    });
}

window.searchIndices = searchIndices;

function toggleColumn(columnType) {
    const isVisible = document.getElementById(`toggle-${columnType}`).checked;
    const metricCells = document.querySelectorAll(`.metric-cell[data-tooltip*="${columnType === 'v1' ? 'V1' : 'Relative Momentum'}"]`);
    const headerSpans = document.querySelectorAll(`.sortable[onclick*="${columnType}"]`);
    
    metricCells.forEach(cell => {
        cell.style.display = isVisible ? '' : 'none';
    });
    
    headerSpans.forEach(span => {
        span.style.display = isVisible ? '' : 'none';
    });
    
    // Adjust metrics grid to only show visible columns
    const metricsGrids = document.querySelectorAll('.metrics-grid');
    metricsGrids.forEach(grid => {
        const visibleColumns = 2 + 
            (document.getElementById('toggle-v1').checked ? 1 : 0) + 
            (document.getElementById('toggle-rmom').checked ? 1 : 0);
        grid.style.gridTemplateColumns = `repeat(${visibleColumns}, 1fr)`;
    });
    
    // Adjust header metrics
    const metricHeaders = document.querySelectorAll('.metric-headers');
    metricHeaders.forEach(header => {
        const visibleColumns = 2 + 
            (document.getElementById('toggle-v1').checked ? 1 : 0) + 
            (document.getElementById('toggle-rmom').checked ? 1 : 0);
        header.style.gridTemplateColumns = `repeat(${visibleColumns}, 1fr)`;
    });
}

window.toggleColumn = toggleColumn;

document.addEventListener('DOMContentLoaded', () => {
    loadData();
    
    const durationSelect = document.getElementById('duration');
    if (durationSelect) {
        durationSelect.addEventListener('change', (e) => {
            console.log('Duration changed to:', e.target.value);
            // Clear existing data
            allData = [];
            const tbody = document.getElementById('table-body');
            if (tbody) tbody.innerHTML = '';
            // Reload data with new duration
            loadData();
        });
    }
});
