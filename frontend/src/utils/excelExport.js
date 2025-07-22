import * as XLSX from 'xlsx';

/**
 * Export matrix data to Excel file
 * @param {Object} matrixData - The matrix data from the backend
 * @param {Object} matrixStatistics - The matrix statistics from the backend
 * @param {string} summary - Summary text to include
 * @param {string} recommendations - Recommendations text to include
 * @param {string} filename - Optional filename (defaults to 'testmind-matrix.xlsx')
 */
export const exportToExcel = (matrixData, matrixStatistics = {}, summary = '', recommendations = '', filename = 'testmind-matrix.xlsx') => {
  const workbook = XLSX.utils.book_new();
  
  // Create matrix worksheet
  const transitions = Object.keys(matrixData);
  const personas = new Set();
  
  transitions.forEach(transition => {
    Object.keys(matrixData[transition]).forEach(persona => {
      personas.add(persona);
    });
  });
  
  const personaArray = Array.from(personas);
  
  // Create matrix data for Excel
  const matrixRows = [];
  
  // Header row
  const headerRow = ['Transition', ...personaArray];
  matrixRows.push(headerRow);
  
  // Data rows
  transitions.forEach(transition => {
    const row = [transition];
    personaArray.forEach(persona => {
      const data = matrixData[transition][persona];
      const status = data?.status || 'Unknown';
      const id = data?.id || '';
      row.push(`${status}${id ? ` (${id})` : ''}`);
    });
    matrixRows.push(row);
  });
  
  // Create matrix worksheet
  const matrixWorksheet = XLSX.utils.aoa_to_sheet(matrixRows);
  
  // Apply cell styling and colors
  const matrixRange = XLSX.utils.decode_range(matrixWorksheet['!ref']);
  
  // Style header row with better colors
  for (let col = 0; col <= matrixRange.e.c; col++) {
    const colLetter = XLSX.utils.encode_col(col);
    const cellRef = `${colLetter}1`;
    if (matrixWorksheet[cellRef]) {
      matrixWorksheet[cellRef].s = { 
        font: { bold: true, color: { rgb: "FFFFFF" }, size: 12 },
        fill: { fgColor: { rgb: "2E75B6" } },
        alignment: { horizontal: "center", vertical: "center" }
      };
    }
  }
  
  // Style data cells with colors based on status
  for (let row = 1; row <= matrixRange.e.r; row++) {
    for (let col = 1; col <= matrixRange.e.c; col++) {
      const colLetter = XLSX.utils.encode_col(col);
      const cellRef = `${colLetter}${row + 1}`;
      if (matrixWorksheet[cellRef]) {
        const cellValue = matrixWorksheet[cellRef].v;
        let fillColor = "FFFFFF"; // Default white
        let fontColor = "000000"; // Default black
        
        if (typeof cellValue === 'string') {
          if (cellValue.includes('Essential')) {
            fillColor = "C6EFCE"; // Light green
            fontColor = "006100"; // Dark green text
          } else if (cellValue.includes('Optional')) {
            fillColor = "FFEB9C"; // Light yellow
            fontColor = "9C6500"; // Dark yellow text
          } else if (cellValue.includes('Prohibited')) {
            fillColor = "FFC7CE"; // Light red
            fontColor = "9C0006"; // Dark red text
          }
        }
        
        matrixWorksheet[cellRef].s = {
          fill: { fgColor: { rgb: fillColor } },
          font: { color: { rgb: fontColor }, bold: cellValue.includes('(') },
          alignment: { horizontal: "center", vertical: "center" },
          border: {
            top: { style: "thin", color: { rgb: "D0D0D0" } },
            bottom: { style: "thin", color: { rgb: "D0D0D0" } },
            left: { style: "thin", color: { rgb: "D0D0D0" } },
            right: { style: "thin", color: { rgb: "D0D0D0" } }
          }
        };
      }
    }
  }
  
  // Style transition column (first column)
  for (let row = 1; row <= matrixRange.e.r; row++) {
    const cellRef = `A${row + 1}`;
    if (matrixWorksheet[cellRef]) {
      matrixWorksheet[cellRef].s = {
        ...matrixWorksheet[cellRef].s,
        font: { bold: true, color: { rgb: "000000" } },
        fill: { fgColor: { rgb: "F2F2F2" } }
      };
    }
  }
  
  XLSX.utils.book_append_sheet(workbook, matrixWorksheet, 'Test Matrix');
  
  // Create statistics worksheet with enhanced styling
  if (matrixStatistics && Object.keys(matrixStatistics).length > 0) {
    const statsData = [
      ['TestMind Matrix Statistics Report'],
      ['Generated on', new Date().toLocaleString()],
      [],
      ['Metric', 'Value', 'Description'],
      ['Total Combinations', matrixStatistics.total_combinations || 0, 'Total possible combinations (transitions × personas)'],
      ['Essential Combinations (Green)', matrixStatistics.essential_combinations || 0, 'Selected for execution with test IDs'],
      ['Optional Combinations (Yellow)', matrixStatistics.optional_combinations || 0, 'Dropped combinations - available for additional testing'],
      ['Prohibited Combinations (Red)', matrixStatistics.prohibited_combinations || 0, 'Prohibited combinations - excluded from testing'],
      ['Total Transitions', matrixStatistics.total_transitions || 0, 'Number of state transitions'],
      ['Total Personas', matrixStatistics.total_personas || 0, 'Number of user personas'],
      [],
      ['Coverage Analysis'],
      ['Essential Coverage', `${matrixStatistics.essential_combinations || 0}/${matrixStatistics.total_combinations || 0} (${Math.round(((matrixStatistics.essential_combinations || 0) / (matrixStatistics.total_combinations || 1)) * 100)}%)`],
      ['Optional Coverage', `${matrixStatistics.optional_combinations || 0}/${matrixStatistics.total_combinations || 0} (${Math.round(((matrixStatistics.optional_combinations || 0) / (matrixStatistics.total_combinations || 1)) * 100)}%)`],
      ['Prohibited Coverage', `${matrixStatistics.prohibited_combinations || 0}/${matrixStatistics.total_combinations || 0} (${Math.round(((matrixStatistics.prohibited_combinations || 0) / (matrixStatistics.total_combinations || 1)) * 100)}%)`],
      [],
      ['Legend'],
      ['Essential (Green)', 'Selected for execution with test IDs - Critical test cases'],
      ['Optional (Yellow)', 'Dropped combinations - Available for additional testing'],
      ['Prohibited (Red)', 'Prohibited combinations - Excluded from testing']
    ];
    
    const statsWorksheet = XLSX.utils.aoa_to_sheet(statsData);
    
    // Style statistics worksheet
    const statsRange = XLSX.utils.decode_range(statsWorksheet['!ref']);
    
    // Style title
    if (statsWorksheet['A1']) {
      statsWorksheet['A1'].s = { 
        font: { bold: true, size: 16, color: { rgb: "2E75B6" } },
        alignment: { horizontal: "center" }
      };
    }
    
    // Style headers
    for (let col = 0; col <= statsRange.e.c; col++) {
      const colLetter = XLSX.utils.encode_col(col);
      const cellRef = `${colLetter}4`; // Metric, Value, Description row
      if (statsWorksheet[cellRef]) {
        statsWorksheet[cellRef].s = { 
          font: { bold: true, color: { rgb: "FFFFFF" } },
          fill: { fgColor: { rgb: "2E75B6" } },
          alignment: { horizontal: "center" }
        };
      }
    }
    
    // Style coverage analysis header
    if (statsWorksheet['A12']) {
      statsWorksheet['A12'].s = { 
        font: { bold: true, size: 14, color: { rgb: "2E75B6" } },
        fill: { fgColor: { rgb: "E7F3FF" } }
      };
    }
    
    // Style legend header
    if (statsWorksheet['A17']) {
      statsWorksheet['A17'].s = { 
        font: { bold: true, size: 14, color: { rgb: "2E75B6" } },
        fill: { fgColor: { rgb: "E7F3FF" } }
      };
    }
    
    // Color-code the metric values
    const essentialCell = statsWorksheet['B6'];
    const optionalCell = statsWorksheet['B7'];
    const prohibitedCell = statsWorksheet['B8'];
    
    if (essentialCell) {
      essentialCell.s = { 
        font: { bold: true, color: { rgb: "006100" } },
        fill: { fgColor: { rgb: "C6EFCE" } }
      };
    }
    
    if (optionalCell) {
      optionalCell.s = { 
        font: { bold: true, color: { rgb: "9C6500" } },
        fill: { fgColor: { rgb: "FFEB9C" } }
      };
    }
    
    if (prohibitedCell) {
      prohibitedCell.s = { 
        font: { bold: true, color: { rgb: "9C0006" } },
        fill: { fgColor: { rgb: "FFC7CE" } }
      };
    }
    
    XLSX.utils.book_append_sheet(workbook, statsWorksheet, 'Statistics');
  }
  
  // Create summary worksheet
  if (summary || recommendations) {
    const summaryData = [];
    
    if (summary) {
      summaryData.push(['TestMind Summary Report']);
      summaryData.push(['Generated on', new Date().toLocaleString()]);
      summaryData.push([]);
      summaryData.push(['Summary']);
      summaryData.push([summary]);
      summaryData.push([]); // Empty row
    }
    
    if (recommendations) {
      summaryData.push(['Recommendations']);
      summaryData.push([recommendations]);
    }
    
    const summaryWorksheet = XLSX.utils.aoa_to_sheet(summaryData);
    
    // Style summary worksheet
    if (summaryWorksheet['A1']) {
      summaryWorksheet['A1'].s = { 
        font: { bold: true, size: 16, color: { rgb: "2E75B6" } }
      };
    }
    
    XLSX.utils.book_append_sheet(workbook, summaryWorksheet, 'Summary');
  }
  
  // Create metadata worksheet
  const metadata = [
    ['TestMind Matrix Metadata'],
    ['Generated by', 'TestMind AI'],
    ['Generated on', new Date().toLocaleString()],
    ['Total Transitions', transitions.length],
    ['Total Personas', personaArray.length],
    ['Total Test Cases', transitions.length * personaArray.length],
    [],
    ['Transitions'],
    ...transitions.map(t => [t]),
    [],
    ['Personas'],
    ...personaArray.map(p => [p])
  ];
  
  const metadataWorksheet = XLSX.utils.aoa_to_sheet(metadata);
  
  // Style metadata worksheet
  if (metadataWorksheet['A1']) {
    metadataWorksheet['A1'].s = { 
      font: { bold: true, size: 16, color: { rgb: "2E75B6" } }
    };
  }
  
  XLSX.utils.book_append_sheet(workbook, metadataWorksheet, 'Metadata');
  
  // Export the file
  XLSX.writeFile(workbook, filename);
};

/**
 * Export conversation history to Excel
 * @param {Array} messages - Array of message objects
 * @param {string} filename - Optional filename (defaults to 'testmind-conversation.xlsx')
 */
export const exportConversationToExcel = (messages, filename = 'testmind-conversation.xlsx') => {
  const workbook = XLSX.utils.book_new();
  
  const conversationData = [
    ['Timestamp', 'Sender', 'Type', 'Content']
  ];
  
  messages.forEach(message => {
    let content = '';
    if (message.type === 'bot' && message.content.status === 'success') {
      content = `Summary: ${message.content.summary || 'N/A'}\n\nMatrix Data: ${JSON.stringify(message.content.matrix_data, null, 2)}`;
    } else if (message.type === 'bot' && message.content.status === 'conversation') {
      content = message.content.response || 'N/A';
    } else {
      content = message.content;
    }
    
    conversationData.push([
      message.timestamp,
      message.type === 'bot' ? 'TestMind AI' : 'User',
      message.type,
      content
    ]);
  });
  
  const worksheet = XLSX.utils.aoa_to_sheet(conversationData);
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Conversation');
  
  // Auto-size columns
  const range = XLSX.utils.decode_range(worksheet['!ref']);
  for (let col = 0; col <= range.e.c; col++) {
    const colLetter = XLSX.utils.encode_col(col);
    worksheet[`${colLetter}1`] = { 
      ...worksheet[`${colLetter}1`],
      s: { font: { bold: true } }
    };
  }
  
  XLSX.writeFile(workbook, filename);
}; 