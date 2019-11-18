# SkyTrak Import

Quick and dirty import of SkyTrak session data into a SQL database

### Libraries/Packages

- pandas
- sqlalchemy
- urllib
- pyodbc

### SQL Schema

~~~~
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Shots]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[Shots](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[OverallShotNumber] [int] NOT NULL,
	[ClubShotNumber] [int] NOT NULL,
	[Club] [varchar](2) NOT NULL,
	[Hand] [varchar](1) NOT NULL,
	[BallSpeed] [decimal](18, 2) NOT NULL,
	[LaunchAngle] [decimal](18, 2) NOT NULL,
	[Backspin] [decimal](18, 2) NOT NULL,
	[Sidespin] [decimal](18, 2) NOT NULL,
	[SideDegree] [decimal](18, 2) NOT NULL,
	[OfflineYardage] [decimal](18, 2) NOT NULL,
	[CarryYardage] [decimal](18, 2) NOT NULL,
	[RollYardage] [decimal](18, 2) NOT NULL,
	[TotalYardage] [decimal](18, 2) NOT NULL,
	[FlightTime] [decimal](18, 2) NOT NULL,
	[DescentDegree] [decimal](18, 2) NOT NULL,
	[HeightYardage] [decimal](18, 2) NOT NULL,
	[ClubSpeed] [decimal](18, 2) NOT NULL,
	[PTIScore] [decimal](18, 2) NOT NULL,
	[TakenOn] [datetime] NOT NULL,
 CONSTRAINT [PK_Shots] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
~~~~