import React from "react";

const OpLog = () => {
    return (
        <div className="flex w-full h-full">
            <iframe src="http://localhost:3001/d/Airflow_Monitor/airflow-monitoring?orgId=1&from=1685715567969&to=1685888367970&theme=light&refresh=5s&kiosk" frameborder="0" className="w-full h-full"></iframe>
        </div>
    );
};

export default OpLog;