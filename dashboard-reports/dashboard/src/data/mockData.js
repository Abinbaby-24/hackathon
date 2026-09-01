export const inspections = [
  {
    id: 101,
    productName: "ABC Rice",
    date: "01-09-2026",
    status: "Non-Compliant",
    complianceScore: 72,
    violations: ["Missing MRP", "Missing Manufacturer Address"],
  },
  {
    id: 100,
    productName: "XYZ Cooking Oil",
    date: "31-08-2026",
    status: "Compliant",
    complianceScore: 100,
    violations: [],
  },
  {
    id: 99,
    productName: "Fresh Soap",
    date: "30-08-2026",
    status: "Compliant",
    complianceScore: 95,
    violations: [],
  },
  {
    id: 98,
    productName: "Daily Wheat Flour",
    date: "29-08-2026",
    status: "Non-Compliant",
    complianceScore: 68,
    violations: ["Missing Net Quantity"],
  },
  {
    id: 97,
    productName: "Pure Sugar",
    date: "28-08-2026",
    status: "Compliant",
    complianceScore: 100,
    violations: [],
  },
];

export const violationData = [
  {
    name: "Missing MRP",
    count: 8,
  },
  {
    name: "Missing Manufacturer",
    count: 5,
  },
  {
    name: "Missing Quantity",
    count: 4,
  },
  {
    name: "Missing Date",
    count: 2,
  },
];

export const dashboardStats = {
  totalInspections: 42,
  compliant: 31,
  nonCompliant: 11,
  complianceRate: 73.8,
};