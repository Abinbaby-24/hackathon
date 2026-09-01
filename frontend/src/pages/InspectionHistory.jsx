import { useEffect, useState } from "react";

import MainLayout from "../layouts/MainLayout";
import api from "../services/api";

function InspectionHistory() {

  const [inspections, setInspections] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {

    const fetchInspections = async () => {

      try {

        const response =
          await api.get("/inspections");

        console.log(
          "Inspections:",
          response.data
        );

        const data =
          response.data.inspections ||
          response.data.data ||
          response.data;

        setInspections(
          Array.isArray(data) ? data : []
        );

      } catch (err) {

        console.error(err);

        setError(
          "Unable to load inspection history."
        );

      } finally {

        setLoading(false);

      }

    };

    fetchInspections();

  }, []);


  return (
    <MainLayout>

      <div className="page-header">

        <div>
          <h1>Inspection History</h1>

          <p>
            View previous package inspections
          </p>
        </div>

      </div>

      {loading && (
        <p>Loading inspections...</p>
      )}

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {!loading && !error && (

        <div className="table-container">

          <table>

            <thead>

              <tr>
                <th>ID</th>
                <th>Product</th>
                <th>Score</th>
                <th>Status</th>
                <th>Date</th>
              </tr>

            </thead>

            <tbody>

              {inspections.length === 0 ? (

                <tr>
                  <td colSpan="5">
                    No inspections found.
                  </td>
                </tr>

              ) : (

                inspections.map(
                  (inspection, index) => (

                    <tr key={inspection.id || index}>

                      <td>
                        {inspection.id ||
                          inspection.inspection_id}
                      </td>

                      <td>
                        {inspection.product_name ||
                          inspection.product?.product_name ||
                          "Unknown"}
                      </td>

                      <td>
                        {inspection.score ?? "N/A"}
                      </td>

                      <td>
                        {inspection.status || "N/A"}
                      </td>

                      <td>
                        {inspection.created_at ||
                          inspection.date ||
                          "N/A"}
                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      )}

    </MainLayout>
  );
}

export default InspectionHistory;