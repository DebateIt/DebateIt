import '@fontsource/bebas-neue';
import '@fontsource/nunito';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { ThemeProvider } from '@mui/material/styles';

import theme from '../Theme';

function NavBar() {
	return (
		<ThemeProvider theme={theme}>
			<Drawer
				variant="persistent"
				anchor="left"
				open={true}
				sx={{
					padding: 0,
					height: '100%'
				}}
			>
				<Box
					component="nav"
					sx={{
						width: 250,
						bgcolor: 'secondary.main',
						height: '100%'
					}}
				>
					<List>
						<ListItem key="-2">
							<ListItemText
								primary={
									<Typography
										variant="h4"
										component="div"
										align="center"
										sx={{
											fontFamily: "Bebas Neue",
											color: "info.main"
										}}
									>
										DebateIt
									</Typography>
								}
							/>
						</ListItem>
						<ListItem key="-1">
							<ListItemText
								primary={
									<Typography
										variant="h6"
										component="div"
										align="center"
										mt={4}
										mb={4}
										sx={{
											fontFamily: "Bebas Neue",
											color: "info.main"
										}}
									>
										ALPACAMAX
									</Typography>
								}
							/>
						</ListItem>
						{["Yours", "Topics", "Debates"].map((text, index) => (
							<ListItem button key={index}>
								<ListItemText
									primary={
										<Typography
											component="div"
											align="center"
											sx={{
												fontFamily: "Nunito",
												color: "info.main"
											}}
										>
											{text}
										</Typography>
									}
								/>
							</ListItem>
						))}
					</List>
				</Box>
			</Drawer>
		</ThemeProvider>
	);
};

export default NavBar;