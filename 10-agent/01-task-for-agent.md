# **E-commerce Analytics Streamlit App - Development Plan for Claude Code**

## **Project Overview**

A single-page data analytics tool using Streamlit that allows users to ask business questions about e-commerce data through a clean dropdown interface and receive rich, multi-modal insights combining text explanations and interactive visualizations. The application features a clean sidebar navigation and immediate inline results display.

## **Pre-Development Setup**

### **Database Preparation (One-Time Activity)**

- Execute the provided `20-config/01-data_generator.py` script to create `30-database/my_ecommerce_db.duckdb`
- Verify database contains 10,000 e-commerce orders with complete schema
- Add the database file to the repository for direct use by the application
- Document the schema structure for LLM integration

### **Environment Configuration**

- **Local Development:** Use `.env` file with required environment variables
- **Production Deployment:** Configure Streamlit secrets for API key and relative database path
- Set up proper environment variable handling for both scenarios

#### **Required Environment Variables**

```bash
# Required .env variables (create .env.example template)
OPENAI_API_KEY=your_api_key_here
DUCKDB_PATH=30-database/my_ecommerce_db.duckdb
STREAMLIT_THEME=light
LOG_LEVEL=INFO
CACHE_TTL=300  # 5 minutes
MAX_QUERY_ROWS=10000
QUERY_TIMEOUT=30
NUM_ORDERS=10000
NUM_CUSTOMERS=500
START_DATE=2023-01-01
END_DATE=2023-12-31
DB_OUTPUT_PATH=30-database/my_ecommerce_db.duckdb
```

### **Create & Activate Virtual Environment**

- Create the venv once using the command:

  ```bash
  python3 -m venv venv
  ```

- For each session, activate the venv using:

  ```bash
  source venv/bin/activate
  ```

- Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

### **Database Schema Documentation Requirements**

Create comprehensive schema documentation including:

- Complete data dictionary with business definitions for each column
- Sample queries demonstrating table/column usage
- Data quality constraints and assumptions
- Relationship diagrams showing data flow
- Query performance considerations and indexing strategy
- Data validation rules and business logic constraints

---

## **Current Phase: Enhanced UI & Experience (Phase 1.5)**

The core MVP functionality is largely complete. Focus is now on UI refinements and user experience improvements.

### **1.1 Current Project Structure**

The project currently has this structure:

```
Data-Story-AI/
├── Welcome.py                 # Main Streamlit entry point
├── pages/                     # Streamlit multi-page app structure
│   ├── Analysis.py           # Main analysis interface (single-page)
│   └── Data.py               # Data overview and schema information
├── 10-agent/                  # Agent instructions and workflows
│   ├── 01-task-for-agent.md
│   ├── 02-instructions-for-agent.md
│   ├── 03-task-state-tracker.md
│   └── 04-response_guidelines.md
├── 20-config/                 # Data generation and configuration
│   └── 01-data_generator.py  # Generates synthetic e-commerce data
├── 30-database/               # Database utilities and schema
│   ├── __init__.py
│   ├── connection.py          # DuckDB connection utilities
│   ├── schema.py             # Schema definitions for LLM context
│   └── my_ecommerce_db.duckdb # Generated database (10K orders)
├── 40-llm/                    # LLM integration components
│   ├── sql_agent.py          # LangChain SQL agent
│   └── story_generator.py    # OpenAI story generation
├── 50-visualization/          # Visualization components
│   └── plotly_charts.py      # Interactive chart generation
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── test_application.py        # Application tests
├── good-layout.png            # UI design reference
└── venv/                     # Python virtual environment
```

### **📁 Recommended File Structure Improvements**

```
Data-Story-AI/
├── app.py                     # Rename Welcome.py to app.py (clearer entry point)
├── pages/
│   ├── 01_Analysis.py         # Rename with numbers for better ordering
│   └── 02_Data.py
├── src/                       # Move core modules into src/
│   ├── database/              # Rename 30-database -> src/database
│   ├── llm/                   # Rename 40-llm -> src/llm
│   └── visualization/         # Rename 50-visualization -> src/visualization
├── config/                    # Rename 20-config -> config
├── docs/                      # Rename 10-agent -> docs
├── data/                      # New: For database files and datasets
│   └── my_ecommerce_db.duckdb
├── tests/                     # Proper testing structure
├── .env.example              # Environment variable template
└── .gitignore                # Updated to exclude .env files
```

### **1.2 Database Integration**

- Create connection utilities for DuckDB with proper error handling
- Define comprehensive schema information for LLM context including:
  - Complete column definitions with types and business meanings
  - Sample data rows for reference and validation
  - Business context for each field with examples
  - Relationships and constraints between tables/fields
  - Performance optimization hints for common queries
- Implement basic query execution functions with timeout and result limits
- Add connection testing, validation, and health checks
- Create data validation functions for quality assurance

### **1.3 Single-Page Streamlit Interface**

- Create single-page layout with clean sidebar navigation
- **Main Interface:**
  - Dropdown selection for pre-populated questions
  - "Other" option for custom question input
  - Immediate inline display of analysis results
  - Clean, minimal interface focused on single-turn interactions
  - Input sanitization and basic validation
- **Sidebar Navigation:**
  - Clean navigation between Welcome, Analysis, and Data pages
  - Minimal, professional styling
- **Results Display:**
  - Inline results display below question selection
  - Loading state indicators with progress tracking
  - Error boundary components for graceful failure handling

### **1.4 LangChain SQL Agent Integration**

- Configure LangChain SQL agent with OpenAI API
- Provide detailed schema context to the agent with examples
- Implement basic query generation and execution with validation
- Add fundamental error handling for invalid SQL with retry mechanisms
- Test with simple queries to verify functionality
- Implement query result caching and performance monitoring

### **1.5 Basic Error Handling**

- Wrap all external API calls in try-catch blocks with specific error types
- Implement user-friendly error messages (no technical jargon)
- Add comprehensive logging for debugging with proper log levels
- Create fallback responses for common failure scenarios
- Implement circuit breaker patterns for external dependencies
- Add retry mechanisms with exponential backoff

---

## **Phase 2: Rich Content Generation (Completed)**

The rich content generation is implemented and working:

### **2.1 Story Generation Framework**

- Design structured prompt templates for consistent LLM responses
- Implement response format with:
  - Executive summary (2-3 sentences)
  - Key insights (3-5 bullet points)
  - Visualization specifications with clear parameters
  - Explanatory context and business implications
- Add few-shot learning examples in prompts with diverse scenarios
- Implement JSON response parsing and validation with error recovery
- Create prompt optimization and A/B testing framework

### **2.2 Visualization Strategy Implementation**

**Mermaid Diagrams - For Process/Conceptual Visualization:**

- Business processes (order workflows, customer journeys)
- Hierarchical relationships (category → subcategory → product)
- Decision trees and flowcharts
- Conceptual frameworks and business logic flows

**Plotly Charts - For Data Visualization:**

- Time series analysis (sales trends, seasonal patterns)
- Categorical comparisons (product categories, states, payment methods)
- Distribution analysis (price ranges, order values, customer segments)
- Correlation visualizations (price vs quantity relationships)
- Geographic visualizations (sales by state/region)

### **2.3 Content Integration**

- Implement View tab content generation pipeline with proper sequencing
- Create dynamic content rendering based on query results
- Add proper spacing and formatting for multi-modal content
- Implement complete redraw functionality for new questions
- Add content validation and quality checks
- Create responsive design for different screen sizes

---

## **Current Implementation Status**

### **✅ Completed Features**
- Single-page interface with dropdown question selection
- Pre-populated business questions for e-commerce analytics
- Inline results display with visualizations
- Database integration with 10,000 sample orders
- Clean sidebar navigation between pages
- LLM-powered SQL generation and story creation
- Interactive Plotly charts and data tables

### **📋 Remaining Improvements**
- UI refinements to match target design (dropdown styling, layout optimization)
- Enhanced error handling and user feedback
- Performance optimization for larger datasets
- Additional pre-populated questions for different business scenarios
- Query result caching for improved response times

---

## **Security Considerations**

### **Input Security**

- Sanitize all user inputs to prevent injection attacks
- Validate query parameters and SQL generation
- Implement rate limiting for API calls and user requests
- Add CSRF protection for form submissions

### **API Security**

- Secure API key storage and rotation procedures
- Implement proper authentication and authorization
- Monitor API usage and detect anomalous patterns
- Add request signing and validation

### **Data Security**

- Encrypt sensitive data at rest and in transit
- Implement proper access controls and audit logging
- Regular security scans and vulnerability assessments
- Data privacy compliance (GDPR, CCPA considerations)

---

## **Key Technical Decisions & Rationale**

### **Data Strategy**

- **Pre-built Database:** Eliminates runtime data generation complexity and ensures consistent testing environment
- **DuckDB Choice:** Optimized for analytical queries, better performance than SQLite for aggregations
- **Schema Documentation:** Comprehensive context improves LLM query accuracy and reduces errors

### **Architecture Decisions**

- **Single-Page Interface:** Streamlined user experience with dropdown question selection and inline results
- **Multi-Page Streamlit App:** Clean navigation between Welcome, Analysis, and Data overview pages
- **Modular Component Design:** Separate modules for database, LLM, and visualization logic
- **Single-Turn Interactions:** Focus on immediate question-answer workflow without complex state management
- **Inline Results Display:** Complete analysis results shown immediately below question selection

### **LLM Integration Approach**

- **Schema-Aware Agent:** Providing complete schema context improves query accuracy
- **Structured Responses:** JSON format ensures consistent parsing and display
- **Visualization Separation:** Clear roles for Mermaid (conceptual) vs Plotly (data) reduces confusion
- **Error Recovery:** Multiple fallback strategies for robust operation

---

## **Identified Risks & Mitigation Strategies**

### **High Priority Risks**

1. **Invalid SQL Generation:** Mitigated by validation, retry mechanisms, comprehensive schema context, and query testing
2. **API Rate Limits:** Handled through exponential backoff, circuit breaker patterns, and usage monitoring
3. **Performance Issues:** Addressed via result limits, timeouts, strategic caching, and performance monitoring
4. **Security Vulnerabilities:** Prevented through input validation, secure coding practices, and regular security audits

### **Medium Priority Concerns**

1. **Question Complexity:** Managed through user guidance, complexity analysis, and query decomposition
2. **Visualization Syntax Errors:** Reduced via prompt engineering, validation, and error recovery
3. **User Experience Flow:** Enhanced through progressive loading, clear feedback, and accessibility features
4. **Data Quality Issues:** Addressed through validation, constraints, and quality monitoring

### **Monitoring & Improvement**

- Log all failed queries for prompt improvement and pattern analysis
- Track user question patterns for feature enhancement and optimization
- Monitor API usage and performance metrics with alerting
- Collect user feedback for iterative improvements and feature requests
- Implement A/B testing for prompt optimization and UI improvements

---

## **Success Criteria**

### **Functional Requirements**

- Users can ask natural language questions about e-commerce data with 95% success rate
- System generates accurate SQL queries for business questions with proper error handling
- Rich stories combine text insights with relevant visualizations consistently
- Application handles common error scenarios gracefully without crashes
- Response time under 30 seconds for 90% of queries

### **Performance Requirements**

- Query responses within 30 seconds for typical questions
- Successful visualization generation for 90%+ of valid queries
- Stable operation under normal usage patterns (50+ concurrent users)
- Memory usage under 1GB for typical workloads
- 99.5% uptime during business hours

### **User Experience Goals**

- Intuitive interface requiring minimal learning curve (< 5 minutes to first success)
- Clear feedback during processing operations with progress indicators
- Meaningful error messages and recovery suggestions
- Engaging and informative data stories that provide business value
- Accessible design meeting WCAG 2.1 AA standards

### **Security & Compliance Goals**

- No security vulnerabilities in production deployment
- Proper data handling and privacy protection
- Audit trail for all user actions and system operations
- Compliance with relevant data protection regulations

This plan provides Claude Code with a comprehensive roadmap while maintaining flexibility for implementation decisions and iterative development approaches. The enhanced specifications should significantly improve the robustness and production-readiness of the final application.
