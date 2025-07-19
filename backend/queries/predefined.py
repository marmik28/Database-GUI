from flask import jsonify
from sqlalchemy import text

def register_predefined_routes(app, db):

    @app.route('/api/query/1')
    def query_1():
        sql = text("""
        SELECT 
            l.LocationID,
            l.Name AS LocationName,
            l.Address,
            l.City,
            l.Province,
            l.PostalCode,
            l.Phone,
            l.WebAddress,
            l.Type,
            l.Capacity,
            (
                SELECT CONCAT(p.FirstName, ' ', p.LastName)
                FROM Personnel p
                JOIN Personnel_Location_History plh ON p.PersonnelID = plh.PersonnelID
                WHERE plh.LocationID = l.LocationID
                  AND p.RoleID = 1
                  AND plh.EndDate IS NULL
                LIMIT 1
            ) AS GeneralManagerName,
            (
                SELECT COUNT(*) FROM Personnel_Location_History plh
                WHERE plh.LocationID = l.LocationID AND plh.EndDate IS NULL
            ) AS PersonnelCount,
            (
                SELECT COUNT(*) FROM ClubMembers cm
                WHERE cm.LocationID = l.LocationID
            ) AS ClubMemberCount
        FROM Locations l
        ORDER BY ClubMemberCount DESC;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])

    @app.route('/api/query/2')
    def query_2():
        sql = text("""
        SELECT 
            cm.LocationID AS ClubLocationID,
            l1.Name AS ClubLocationName,
            cm.MemberID,
            cm.FirstName,
            cm.LastName,
            DATE_PART('year', AGE(cm.DOB)) AS Age,
            cm.City,
            cm.Province,
            cm.Status,
            l2.Name AS WorkingLocationName
        FROM ClubMembers cm
        JOIN Personnel p ON cm.SSN = p.SSN
        JOIN Personnel_Location_History plh ON p.PersonnelID = plh.PersonnelID
        JOIN Locations l1 ON cm.LocationID = l1.LocationID
        JOIN Locations l2 ON plh.LocationID = l2.LocationID
        WHERE DATE_PART('year', AGE(cm.DOB)) >= 18
          AND plh.EndDate IS NULL
        ORDER BY l2.Name ASC, Age ASC;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])

    @app.route('/api/query/3')
    def query_3():
        sql = text("""
        SELECT 
            l.Name AS LocationName,
            cm.MemberID,
            cm.FirstName,
            cm.LastName,
            DATE_PART('year', AGE(cm.DOB)) AS Age,
            cm.City,
            cm.Province,
            cm.Status,
            COUNT(mh.HobbyID) AS HobbyCount
        FROM ClubMembers cm
        JOIN Member_Hobby mh ON cm.MemberID = mh.MemberID
        JOIN Locations l ON cm.LocationID = l.LocationID
        GROUP BY l.Name, cm.MemberID
        HAVING COUNT(mh.HobbyID) >= 3
        ORDER BY Age DESC, LocationName ASC;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])

    @app.route('/api/query/4')
    def query_4():
        sql = text("""
        SELECT 
            l.Name AS LocationName,
            cm.MemberID,
            cm.FirstName,
            cm.LastName,
            DATE_PART('year', AGE(cm.DOB)) AS Age,
            cm.City,
            cm.Province,
            cm.Status
        FROM ClubMembers cm
        LEFT JOIN Member_Hobby mh ON cm.MemberID = mh.MemberID
        JOIN Locations l ON cm.LocationID = l.LocationID
        WHERE mh.MemberID IS NULL
        ORDER BY LocationName ASC, Age ASC;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])

    @app.route('/api/query/5')
    def query_5():
        sql = text("""
        SELECT 
            DATE_PART('year', AGE(DOB)) AS Age,
            COUNT(*) AS MemberCount
        FROM ClubMembers
        GROUP BY Age
        ORDER BY Age ASC;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])

    @app.route('/api/query/6')
    def query_6():
        sql = text("""
        SELECT 
            cm_major.FirstName AS MajorFirstName,
            cm_major.LastName AS MajorLastName,
            cm_child.MemberID AS AssociatedMemberID,
            cm_child.FirstName AS ChildFirstName,
            cm_child.LastName AS ChildLastName,
            cm_child.DOB,
            cm_child.SSN,
            cm_child.MedicareCard,
            cm_child.Phone,
            cm_child.Address,
            cm_child.City,
            cm_child.Province,
            cm_child.PostalCode,
            fmc.Relationship,
            cm_child.Status
        FROM ClubMembers cm_major
        JOIN FamilyMembers fm ON cm_major.SSN = fm.SSN
        JOIN FamilyMember_Child fmc ON fm.FamilyID = fmc.FamilyID
        JOIN ClubMembers cm_child ON cm_child.MemberID = fmc.MemberID
        WHERE DATE_PART('year', AGE(cm_major.DOB)) >= 18;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])

    @app.route('/api/query/7')
    def query_7():
        sql = text("""
        SELECT
            SUM(CASE 
                WHEN total.TotalPaid > 200 THEN 200 
                ELSE total.TotalPaid 
            END) AS TotalMembershipFees,
            SUM(CASE 
                WHEN total.TotalPaid > 200 THEN total.TotalPaid - 200 
                ELSE 0 
            END) AS TotalDonations
        FROM (
            SELECT 
                cm.MemberID,
                SUM(p.Amount) AS TotalPaid
            FROM ClubMembers cm
            JOIN Payments p ON cm.MemberID = p.MemberID
            WHERE DATE_PART('year', AGE(cm.DOB)) >= 18
              AND p.MembershipYear BETWEEN 2020 AND 2024
            GROUP BY cm.MemberID
        ) AS total;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])

    @app.route('/api/query/8')
    def query_8():
        sql = text("""
        SELECT 
            l.Name AS LocationName,
            cm.MemberID,
            cm.FirstName,
            cm.LastName,
            DATE_PART('year', AGE(cm.DOB)) AS Age,
            cm.City,
            cm.Province,
            (
                CASE 
                    WHEN DATE_PART('year', AGE(cm.DOB)) >= 18 THEN 200
                    ELSE 100
                END - COALESCE(SUM(p.Amount), 0)
            ) AS AmountDue
        FROM ClubMembers cm
        JOIN Locations l ON cm.LocationID = l.LocationID
        LEFT JOIN Payments p ON cm.MemberID = p.MemberID AND p.MembershipYear = 2025
        WHERE cm.Status = 'Inactive'
        GROUP BY l.Name, cm.MemberID
        ORDER BY LocationName ASC, Age ASC;
        """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])
    
    @app.route('/api/query/9')
    def query_9():
        sql = text("""
                   SELECT * From locations;
                   """)
        result = db.session.execute(sql).mappings()
        return jsonify([dict(row) for row in result])
