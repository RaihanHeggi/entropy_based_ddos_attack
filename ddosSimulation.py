from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        h1 = self.addHost( 'h1', ip='10.0.0.1/24' )
        h2 = self.addHost( 'h2', ip='10.0.0.2/24' )
        h3 = self.addHost( 'h3', ip='10.0.0.3/24' )
        h4 = self.addHost( 'h4', ip='10.0.0.4/24' )
        h5 = self.addHost('h5', ip='10.0.0.5/24')
        h6 = self.addHost('h6', ip='10.0.0.6/24')
        h7 = self.addHost('h7', ip='10.0.0.7/24')
        h8 = self.addHost('h8', ip='10.0.0.8/24')
        h9 = self.addHost('h9', ip='10.0.0.9/24')
        h10 = self.addHost('h10', ip='10.0.0.10/24')

        h11 = self.addHost( 'h11', ip='10.0.0.11/24' )
        h12 = self.addHost( 'h12', ip='10.0.0.12/24' )
        h13 = self.addHost( 'h13', ip='10.0.0.13/24' )
        h14 = self.addHost( 'h14', ip='10.0.0.14/24' )
        h15 = self.addHost('h15', ip='10.0.0.15/24')
        h16 = self.addHost('h16', ip='10.0.0.16/24')
        h17 = self.addHost('h17', ip='10.0.0.17/24')
        h18 = self.addHost('h18', ip='10.0.0.18/24')
        h19 = self.addHost('h19', ip='10.0.0.19/24')
        h20 = self.addHost('h20', ip='10.0.0.20/24')
        

        h21 = self.addHost( 'h21', ip='10.0.0.21/24' )
        h22 = self.addHost( 'h22', ip='10.0.0.22/24' )
        h23 = self.addHost( 'h23', ip='10.0.0.23/24' )
        h24 = self.addHost( 'h24', ip='10.0.0.24/24' )
        h25 = self.addHost('h25', ip='10.0.0.25/24')
        h26 = self.addHost('h26', ip='10.0.0.26/24')
        h27 = self.addHost('h27', ip='10.0.0.27/24')
        h28 = self.addHost('h28', ip='10.0.0.28/24')
        h29 = self.addHost('h29', ip='10.0.0.29/24')
        h30 = self.addHost('h30', ip='10.0.0.30/24')

        h31 = self.addHost( 'h31', ip='10.0.0.31/24' )
        h32 = self.addHost( 'h32', ip='10.0.0.32/24' )
        h33 = self.addHost( 'h33', ip='10.0.0.33/24' )
        h34 = self.addHost( 'h34', ip='10.0.0.34/24' )
        h35 = self.addHost('h35', ip='10.0.0.35/24')
        h36 = self.addHost('h36', ip='10.0.0.36/24')
        h37 = self.addHost('h37', ip='10.0.0.37/24')
        h38 = self.addHost('h38', ip='10.0.0.38/24')
        h39 = self.addHost('h39', ip='10.0.0.39/24')
        h40 = self.addHost('h40', ip='10.0.0.40/24')
        
        h41 = self.addHost( 'h41', ip='10.0.0.41/24' )
        h42 = self.addHost( 'h42', ip='10.0.0.42/24' )
        h43 = self.addHost( 'h43', ip='10.0.0.43/24' )
        h44 = self.addHost( 'h44', ip='10.0.0.44/24' )
        h45 = self.addHost('h45', ip='10.0.0.45/24')
        h46 = self.addHost('h46', ip='10.0.0.46/24')
        h47 = self.addHost('h47', ip='10.0.0.47/24')
        h48 = self.addHost('h48', ip='10.0.0.48/24')
        h49 = self.addHost('h49', ip='10.0.0.49/24')
        h50 = self.addHost('h50', ip='10.0.0.50/24')

        # Switches Data
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')
        s4 = self.addSwitch('s4', protocols='OpenFlow13')
        s5 = self.addSwitch('s5', protocols='OpenFlow13')
        s6 = self.addSwitch('s6', protocols='OpenFlow13')
        s7 = self.addSwitch('s7', protocols='OpenFlow13')
        s8 = self.addSwitch('s8', protocols='OpenFlow13')
        s9 = self.addSwitch('s9', protocols='OpenFlow13')
        s10 = self.addSwitch('s10', protocols='OpenFlow13')

        # Add links
        self.addLink(s1,h1)
        self.addLink(s1,h2)
        self.addLink(s1,h3)
        self.addLink(s1,h4)
        self.addLink(s1,h5)

        self.addLink(s2,h6)
        self.addLink(s2,h7)
        self.addLink(s2,h8)
        self.addLink(s2,h9)
        self.addLink(s2,h10)
        
        self.addLink(s3,h11)
        self.addLink(s3,h12)
        self.addLink(s3,h13)
        self.addLink(s3,h14)
        self.addLink(s3,h15)

        self.addLink(s4,h16)
        self.addLink(s4,h17)
        self.addLink(s4,h18)
        self.addLink(s4,h19)
        self.addLink(s4,h20)

        self.addLink(s5,h21)
        self.addLink(s5,h22)
        self.addLink(s5,h23)
        self.addLink(s5,h24)
        self.addLink(s5,h25)

        self.addLink(s6,h26)
        self.addLink(s6,h27)
        self.addLink(s6,h28)
        self.addLink(s6,h29)
        self.addLink(s6,h30)

        self.addLink(s7,h31)
        self.addLink(s7,h32)
        self.addLink(s7,h33)
        self.addLink(s7,h34)
        self.addLink(s7,h35)

        self.addLink(s8,h36)
        self.addLink(s8,h37)
        self.addLink(s8,h38)
        self.addLink(s8,h39)
        self.addLink(s8,h40)

        self.addLink(s9,h41)
        self.addLink(s9,h42)
        self.addLink(s9,h43)
        self.addLink(s9,h44)
        self.addLink(s9,h45)
        
        self.addLink(s10,h46)
        self.addLink(s10,h47)
        self.addLink(s10,h48)
        self.addLink(s10,h49)
        self.addLink(s10,h50)

    
topos = { 'dosTopo': ( lambda: MyTopo() ) }
